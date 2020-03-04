import sys
from typing import Set, Dict, List

from multimethod import overload
import llvmlite.ir as ll
from src.exceptions import *
from src.llvm_ast import next_id, INTRINSIC_FUNC_NAMES
from multi_key_dict import multi_key_dict

from src.warnings import Warnings


def make_empty_context(ll_mod, hl_module):
    return { 'll_mod': ll_mod, 'hl_mod': hl_module, 'scope': [] }


def make_empty_module(hl_module):
    return {
        'name': hl_module['name'],
        'funcs': [],
        'classes': []
    }


def compile_hl_ast(module, is_main=False):
    ll_mod = make_empty_module(module)
    ctx = make_empty_context(ll_mod, module)

    init_func = add_module_init_func(module, ll_mod, ctx)

    if is_main:
        push_module_main(ll_mod, init_func)

    return ll_mod


def add_module_init_func(module, ll_mod, ctx):
    init_func = push_scope(ctx, f"{module['name']}.$init")
    push_module_idempotency_instr(ctx)

    for instr in module['instrs']:
        compile_hl_instr(instr, ctx)

    push_instr(ctx, { 'op': 'ret_void' })

    # add the init func to the module
    init_func = {
        "name": init_func['name'],
        "args": [],
        "ret": { "type": ll.VoidType() },
        "id": next_id(),
        "instrs": init_func['instrs']
    }

    ll_mod['funcs'].append(init_func)
    return init_func


def push_module_main(ll_mod, init_func):
    argc = ll.IntType(32)
    argv = ll.PointerType(ll.PointerType(ll.IntType(8)))
    ll_mod['funcs'].append({
        'name': 'main',
        'ret': { 'type': ll.IntType(32) },
        'args': [ { 'type': argc }, { 'type': argv } ],
        'instrs': [
            {
                'op': 'call',
                'func': { "id": init_func['id'] },
                'args': []
            },
            { 'op': 'ret', 'value': { 'op': 'const_val', 'value': ll.Constant(ll.IntType(32), 0) } }
        ]
    })


def push_module_idempotency_instr(ctx):
    i1 = ll.IntType(8)
    zero, one = ll.Constant(i1, 0), ll.Constant(i1, 1)

    # declare global is_module_init = False
    global_instr = push_instr(ctx, {
        'op': 'global_var',
        'align': 1,
        'name': '$module.is_init',
        'type': i1,
        'value': zero,
    })

    ref = { 'id': global_instr['id'] }

    # if is_module_init:
    #   return
    # else:
    #   is_module_init = true
    push_instr(ctx, {
        'op': 'if',
        'cond': {
            'op': 'trunc', 'type': ll.IntType(1), 'value': { 'op': 'load', 'ref': ref },
        },
        'true': [{ 'op': 'ret_void' }],
        'false': [{
            'op': 'store',
            'ref': ref,
            'value': { 'op': 'const_val', 'type': i1, 'value': one }
        }]
    })


def push_scope(ctx, new_scope_name:str, is_global:bool=False):
    s = {
        "name": new_scope_name,
        "instrs": [],
        "is_global": is_global,
        "local_vars": multi_key_dict()
    }
    # if this is top level scope, then its a global scope
    ctx['scope'].append(s)
    return s


def get_cur_scope(ctx):
    return ctx['scope'][-1]


def iter_scopes_up(ctx, skip_up=0):
    """Iterate up the scope stack, skip up a certain number of scopes when starting.
    This can be useful for looking far variables or functions defined up the stack chain,
    and `skip_up` can be used to skip current and immediate parent scope."""
    scopes = ctx['scope']
    if skip_up >= len(scopes):
        yield from []
    if skip_up > 0:
        scopes = scopes[:-skip_up]

    yield from reversed(scopes)


def push_instr(ctx, instr):
    if not instr.get('id'):
        instr['id'] = next_id()
    get_cur_scope(ctx)['instrs'].append(instr)
    return instr


def pop_scope(ctx):
    if len(ctx['scope']) == 0:
        raise BuildException("Attempt to pop empty scope stack.")

    return ctx['scope'].pop()


@overload
def compile_hl_instr(ast, ctx):
    ast_op = ast.get('op')
    print(f"[ERROR] unsupported ast node '{ast_op}': ", ast, file=sys.stderr)
    raise Exception(f"Unsupported ast node '{ast_op}'")


def is_op(op_name):
    return lambda ast: isinstance(ast, dict) and ast.get('op') == op_name


def get_local_instr_list(ctx):
    local = ctx['local_scope']
    while local:
        if 'instrs' in local:
            return local['instrs']
        local = local.get('parent')
    raise Exception("Could not find local block with instruction list.")


@overload
def compile_hl_instr(ast:is_op('printf'), ctx):
    args = [ compile_hl_instr(arg, ctx) for arg in ast['args'] ]
    instr = { 'op': 'call', 'intrinsic': 'printf', 'args': args, 'hl_ast': ast }
    return push_instr(ctx, instr)


@overload
def compile_hl_instr(ast:is_op('declare_local'), ctx):
    var_name, var_id = ast['name'], ast['id']
    local_vars = get_cur_scope(ctx)['local_vars']

    if var_name in local_vars or var_id in local_vars:
        Warnings.emit(Warnings.duplicate_var, f"Local variable {var_name} has already been declared.")
        return  # don't overwrite current variable info

    for parent_scope in iter_scopes_up(ctx, skip_up=1):
        parent_locals = parent_scope['local_vars']
        if var_name in parent_locals or var_id in parent_locals:
            Warnings.emit(Warnings.shadow_var, f"Local variable {var_name} shadows variable from parent scope.")
            break  # One warning per variable

    create_local_var(ast, ctx)


def create_local_var(ast, ctx):
    var = {
        'name': ast['name'],
        'id': ast['id'],
        'type': ast['type'],
        'outer_type': ast['type'],
        'hl_ast': ast,
        'hl_type': ast['type']
    }

    local_vars = get_cur_scope(ctx)['local_vars']
    local_vars[var['name']] = var
    local_vars[var['id']] = var

    return var


@overload
def outer_type_union(ctx : dict, type1:set, type2:set) -> Set:
    return add_type_def(ctx, type1 | type2)

@overload
def outer_type_union(ctx, type1:dict, type2:set) -> Set:
    type1_id = add_type_def(type1)
    return outer_type_union(ctx, { type1_id }, type2)

@overload
def outer_type_union(ctx, type1:dict, type2:dict) -> Set[Dict]:
    return add_type_def({ add_type_def(type1), add_type_def(type2) })


@overload
def outer_type_union(ctx, type1:set, type2:dict) -> Set[Dict]:
    return outer_type_union(type2, type1)


def lookup_var(ast, ctx):
    var_name, var_id = ast.get('name'), ast.get('id')
    local_vars = get_cur_scope(ctx)['local_vars']

    if var_id and var_id in local_vars:
        return local_vars[var_id]

    if var_name and var_name in local_vars:
        return local_vars[var_name]

    return None


@overload
def compile_hl_instr(ast:is_op('get_var'), ctx):
    """
    { op: get_var, name: str, [id: str] }
    :param ast:
        + op: "get_var"
        + name: str lookup local with this name
        + id: str lookup local with this id
    :param ctx: dict, current context of code
    :return: None
    """
    var = lookup_var(ast, ctx)

    if var is None:
        print("[ERROR] Undefined variable from ast node: ", ast, file=sys.stderr)
        raise UndefinedVariableError()

    return var


@overload
def compile_hl_instr(ast:is_op('assign'), ctx):
    # left instruction doesn't have to exist
    left = compile_hl_instr(ast['left'], ctx)
    right = compile_hl_instr(ast['right'], ctx)

    assert right['hl_type'] == 'numeric'

    copy_hl_type_info(right)

    if not left.get('ll_ref'):
        left['ll_ref'] = { 'id': left['id'], 'type': right['type'], 'name': left['name'] }
        push_instr(ctx, { 'op': 'alloca', 'ref': left['ll_ref'] })

    store_instr = { 'op': 'store', 'ref': left['ll_ref'] }

    if right.get('op') == 'const_val':
        store_instr['value'] = right
    elif right.get('type') == ll.PointerType:
        store_instr['value'] = { 'op': 'load', 'ref': right }

    push_instr(ctx, store_instr)


def is_symbol(ast):
    return all(k in ast for k in ('name', 'id', 'type'))


def is_literal_instr(instr):
    return isinstance(instr, dict) and instr.get('literal') is True


def is_numeric_instr(instr):
    return is_literal_instr(instr) and instr['type'] == 'numeric'


def is_str_literal_instr(instr):
    return is_literal_instr(instr) and instr['type'] == 'str'


@overload
def compile_hl_instr(ast:is_str_literal_instr, ctx):
    return { 'op': 'const_str', 'value': ast['value'], 'hl_ast': ast, 'hl_type': ast['type'] }


@overload
def compile_hl_instr(ast:is_numeric_instr, ctx):
    subtype = ast['subtype']
    precision = ast['precision']
    dtype = None

    if subtype == 'int':
        dtype = ll.IntType(precision)
    elif subtype == 'float':
        if precision == 16:
            dtype = ll.HalfType()
        elif precision == 32:
            dtype = ll.FloatType()
        elif precision == 64:
            dtype = ll.DoubleType()
    elif subtype == 'bool':
        dtype = ll.IntType(1)

    if dtype is None:
        print(f"[ERROR] Unhandled numeric literal type:", ast)
        raise BuildException("Unhandled numeric type: " + ast['subtype'])

    instr = {
        "op": "const_val",
        "type": dtype,
        "value": ll.Constant(dtype, ast["value"]),
        "hl_ast": ast,
        "hl_type": ast["type"]
    }

    return instr


def make_int(value, precision=32):
    return make_literal(value, type='numeric', subtype='int', precision=precision)


def make_float(value, precision=32):
    return make_literal(value, type='numeric', subtype='float', precision=precision)


def make_bool(value):
    return make_literal(value, type='numeric', subtype='bool', precision=8)


def make_str(value):
    return make_literal(type='str', value=value, all_strict=True)


def make_type(type:str,
              subtype:str=None,
              precision:str=None,
              strict_type:bool=False,
              strict_subtype:bool=False,
              strict_precision:bool=False,
              all_strict:bool=False):

    has_type = type is not None
    has_subtype = subtype is not None
    has_prec = precision is not None

    if has_subtype:
        assert has_type, "Cannot specify 'subtype' without a parent 'type'"

    if has_prec:
        assert has_subtype, "Cannot specify 'precision' without a 'subtype'"

    out = dict(
        type = type,
        subtype = subtype,
        precision = precision,
        # We are strict if "all_strict" is set, or each "strict" flag is set,
        # and the value for that setting is present (can't be strict on None)
        strict_type = (all_strict or strict_type) and has_type,
        strict_subtype = (all_strict or strict_subtype) and has_subtype,
        strict_precision = (all_strict or strict_precision) and has_prec)

    return out


def make_literal(value, all_strict=True, **kwargs):
    # For literals, default to making all strict, we can't modify their type
    out = make_type(all_strict=all_strict, **kwargs)
    out['literal'] = True
    out['value'] = value
    return out


def get_type_id(type_def):
    # Prefer "hl_type" since this will persist past first pass compilation,
    # while "type" may be an llvm type
    type_name = type_def.get('hl_type', type_def['type'])
    if type_name == 'numeric':
        return ('numeric', type_def['subtype'], type_def['precision'])


def make_pointer_type(pointee):
    return make_type("pointer")


def copy_hl_type_info(ast):
    return { k: ast.get(k) for k in ('type', 'hl_ast', 'hl_type') }


class Type:
    def __init__(self):
        pass

    def ll_type(self):
        raise NotImplementedError()

    def is_primitive(self):
        return False

    def equivalent(self, other):
        return other == self

    def to_tuple(self):
        return tuple()


class NumericType(Type):
    def __init__(self,
                 is_int:bool=True,
                 precision:int=32,
                 is_bool:int=False,
                 strict_subtype:bool=False,
                 strict_precision:bool=False,
                 **kwargs):
        super().__init__(**kwargs)
        self.is_int = is_int
        self.is_bool = is_bool
        self.precision = precision
        self.strict_subtype = strict_subtype
        self.strict_precision = strict_precision

    def equivalent(self, other):
        return self.is_int == other.is_int and \
            self.is_bool == other.is_bool and \
            self.precision == other.precision

    def to_tuple(self):
        return (NumericType, self.is_int, self.is_bool, self.precision)

    def ll_type(self):
        if self.is_int:
            return ll.IntType(self.precision)
        elif self.is_bool:
            return ll.IntType(8)

        if self.precision >= 64:
            return ll.DoubleType()
        elif self.precision >= 32:
            return ll.FloatType()
        elif self.precision >= 16:
            return ll.HalfType()

    def is_primitive(self):
        return True


class UnionType(Type):
    def __init__(self, types, **kwargs):
        super().__init__(**kwargs)
        self.types = types

    def equivalent(self, other):
        if not isinstance(other, UnionType):
            return False
        return other.to_tuple() == self.to_tuple()

    def to_tuple(self):
        return tuple(sorted(t.to_tuple() for t in self.types))


class Node:
    def __init__(self, parent=None, children=None, type:Type=None):
        self.parent:"Node" = parent
        self.children:List["Node"] = children or []
        for child in self.children:
            child.parent = self
        self.is_built = False
        self.type:Type = type

    def get_locals(self):
        return self.parent.get_locals() if self.parent else None

    def get_globals(self):
        return self.parent.get_globals() if self.parent else None

    def replace_child(self, node, repl_nodes):
        if not repl_nodes:
            return self.remove(node)

        index_of = self.children.index(node)
        self.children[index_of:index_of+1] = repl_nodes
        for node in repl_nodes:
            node.parent = self

    def remove(self, node):
        self.children.remove(node)

    def add(self, *nodes):
        if nodes:
            for node in nodes:
                node.parent = self
                self.children.append(node)

    def build(self):
        if self.is_built:
            return

        self.before_build()

        while not self.is_built:
            self.is_built = True
            self.before_build_children()

            for child_idx, child in enumerate(self.children):
                self.before_build_child(child_idx, child)
                child.build()

            self.build_inner()

        self.after_build()

    def build_inner(self):
        pass

    def before_build(self):
        pass

    def before_build_children(self):
        pass

    def before_build_child(self, child_idx, child):
        pass

    def after_build(self):
        pass

    def to_ll_ast(self):
        raise NotImplementedError()

    def is_lvalue(self):
        if not self.parent:
            return False
        return self.parent.is_child_lvalue(self)

    def is_rvalue(self):
        if not self.parent:
            return False
        return self.parent.is_child_rvalue(self)

    def is_child_lvalue(self, child):
        return False

    def is_child_rvalue(self, child):
        return True


class Literal(Node):
    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def build_inner(self):
        pass

    def to_ll_ast(self):
        ll_type = self.type.ll_type()
        return { "op": "const_val",
                 "type": ll_type,
                 "value": ll.Constant(ll_type, self.value) }


class StrLiteral(Literal):
    def to_ll_ast(self):
        return { 'op': 'const_str', 'value': self.value }


class Variable:
    def __init__(self, name, type=None, nodes=None):
        self.name = name
        self.nodes = nodes or []
        self.ll_id = next_id()
        self.type = type

    def ll_ref(self):
        if not self.type:
            raise UnknownTypeError(f"Variable {self.name} has undefined type.")

        return { "type": self.type.ll_type(), "id": self.ll_id, "name": self.name }


class DefVar(Node):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def build_inner(self):
        self.var = Variable(self.name, nodes=[self], type=self.type)
        self.get_locals()[self.name] = self.var

    def to_ll_ast(self):
        # TODO: handle classes and malloc here based on type
        return { "op": "alloca", "ref": self.var.ll_ref() }


class BareName(Node):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.var:Variable = None

    def build_inner(self):
        self.var = self.get_locals().get(self.name)
        if not self.var:
            raise UndefinedVariableError(f'Undefined symbol {self.name}')

    def to_ll_ast(self):
        if self.is_rvalue():
            return { "op": "load", "ref": self.var.ll_ref() }
        elif self.is_lvalue():
            return self.var.ll_ref()


class BinaryOp(Node):
    def is_child_lvalue(self, child):
        return child == self.children[0]

    def is_child_rvalue(self, child):
        return child == self.children[1]


class Assign(BinaryOp):
    def build_inner(self):
        left, right = self.children[0:2]

        # TODO: handle non-variable?
        left.var.type = right.type

    def to_ll_ast(self):
        left = self.children[0].to_ll_ast()
        right = self.children[1].to_ll_ast()

        return { 'op': 'store', 'ref': left, 'value': right }


class CallIntrinsic(Node):
    def __init__(self, intrinsic:str=None, **kwargs):
        super().__init__(**kwargs)
        self.intrinsic = intrinsic

    def to_ll_ast(self):
        args = [ child.to_ll_ast() for child in self.children ]
        return { "op": "call", "intrinsic": self.intrinsic, "args": args }


class Printf(CallIntrinsic):
    def __init__(self, **kwargs):
        kwargs['intrinsic'] = 'printf'
        super().__init__(**kwargs)


class VarScope(Node):
    def __init__(self, local_symbols = None, global_symbols = None, **kwargs):
        super().__init__(**kwargs)
        self.global_symbols:Dict[str, Node] = local_symbols or dict()
        self.local_symbols:Dict[str, Node] = global_symbols or dict()

    def get_locals(self):
        return self.local_symbols

    def get_globals(self):
        return self.global_symbols


class Module(VarScope):
    def __init__(self, name, is_main:bool=False, **kwargs):
        super().__init__(**kwargs)
        self.is_main = is_main
        self.name = name

    def to_ll_ast(self):
        self.build()

        instrs = [ child.to_ll_ast() for child in self.children ]
        instrs.append({ 'op': 'ret_void' })

        # wrap instructions into init func, returning void
        init_func_inner = {
            "name": f"module.{self.name}.$init_inner",
            "args": [],
            "ret": { "type": ll.VoidType() },
            "id": next_id(),
            "instrs": instrs
        }
        # Call inner func from an "if module init" check initialize function
        init_func = module_init_func_ll_ast(self.name, init_func_inner['id'])
        funcs = [ init_func_inner, init_func ]

        # Call init from main method if this module is main
        if self.is_main:
            funcs.append(main_method_ll_ast(init_func['id']))

        return { "name": self.name, "instrs": instrs, "funcs": funcs, "classes": [] }


def main_method_ll_ast(entry_func_id):
    argc = ll.IntType(32)
    argv = ll.PointerType(ll.PointerType(ll.IntType(8)))
    return {
        'name': 'main',
        'ret': { 'type': ll.IntType(32) },
        'args': [ { 'type': argc }, { 'type': argv } ],
        'instrs': [
            {
                'op': 'call',
                'func': { "id": entry_func_id },
                'args': []
            },
            { 'op': 'ret', 'value': { 'op': 'const_val', 'value': ll.Constant(ll.IntType(32), 0) } }
        ]
    }


def module_init_func_ll_ast(module_name, entry_func_id):
    i1 = ll.IntType(8)
    zero, one = ll.Constant(i1, 0), ll.Constant(i1, 1)

    # declare global is_module_init = False
    global_instr = {
        'op': 'global_var',
        'align': 1,
        'name': '$module.is_init',
        'type': i1,
        'value': zero,
        'id': next_id()
    }

    ref = { 'id': global_instr['id'] }

    # if is_module_init:
    #   return
    # else:
    #   is_module_init = true
    if_cond = {
        'op': 'if',
        'cond': {
            'op': 'u==',
            'left': { 'op': 'load', 'ref': ref },
            'right': { 'op': 'const_val', 'type': i1, 'value': zero }
        },
        'true': [
            { 'op': 'store', 'ref': ref,
              'value': { 'op': 'const_val', 'type': i1, 'value': one } },
            { 'op': 'call', 'func': { 'id': entry_func_id }, 'args': [] },
            { 'op': 'ret_void' }
        ],
        'false': [ { 'op': 'ret_void' } ]
    }

    return {
        "name": f"module.{module_name}.$init",
        "args": [],
        "ret": { "type": ll.VoidType() },
        "id": next_id(),
        "instrs": [global_instr, if_cond],
    }


def subsume_type(left:Type, right:Type) -> Type:
    """
    Return a new type that makes the left type include the right type.
    :param left: Type source type
    :param right: Type new type to include
    :return: Type type that can handle both right and left types
    """
    if left is None:
        return right

    if left.equivalent(right):
        return left

    if isinstance(left, NumericType) and isinstance(right, NumericType):
        combo_type = left.get_min_numeric_type(right)

    return UnionType(types=[ left, right ])
