import sys
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
    return push_instr(ctx, { 'op': 'call', 'intrinsic': 'printf', 'args': args })


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

    local_vars[var_name] = ast
    local_vars[var_id] = ast


def lookup_var(ast, ctx):
    var_name, var_id = ast.get('name'), ast.get('id')
    local_vars = get_cur_scope()['local_vars']

    if var_id and var_id in local_vars:
        return local_vars[var_id]

    if var_name and var_name in local_vars:
        return local_vars[var_name]

    return None


@overload
def compile_hl_instr(ast:is_op('get_var'), ctx):
    """
    { op: get_var, name: str, [id: str, must_exist: bool] }
    :param ast:
        + op: "get_var"
        + name: str lookup local with this name
        + id: str lookup local with this id
        + must_exist: bool, default True, the local must be defined
    :param ctx: dict, current context of code
    :return: None
    """
    var = lookup_var(ast, ctx)

    if var is None and ast.get('must_exist', True):
        print("[ERROR] Undefined variable from ast node: ", ast, file=sys.stderr)
        raise UndefinedVariableError()

    return var


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
    return { 'op': 'const_str', 'value': ast['value'] }


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

    instr = { "op": "const_val", "type": dtype, "value": ll.Constant(dtype, ast['value']) }

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
