import copy
import re
from typing import List
from collections import OrderedDict
from .variable import Variable, BareName, FuncParamVariable, DefVar
from .node import Node
from .var_scope import VarScope
from .type import Type, VoidType
from .union import UnionType
import llvmlite.ir as ll
from src.exceptions import *
from ..id_utils import next_id, next_tmp_name
from .binding import BindInst
from src.exceptions import *
from .cast import CastType, SubsumeType
from .class_def import *


class FuncType(Type):
    def __init__(self, ret_type, arg_types):
        super().__init__()
        self.ret_type = ret_type
        self.arg_types = arg_types or []

    def to_tuple(self):
        return (FuncType, self.ret_type, *self.arg_types)

    def shortname(self):
        return 'fn'

    def longname(self):
        return 'func'

    def is_primitive(self):
        return False

    def equivalent(self, other):
        return (
            isinstance(other, FuncType) and
            (self.ret_type is None or self.ret_type.equivalent(other.ret_type)) and
            len(other.arg_types) == len(self.arg_types) and
            all(a is None or a.equivalent(b) for a, b in zip(self.arg_types, other.arg_types))
        )

    def subsumes(self, other):
        return (
            isinstance(other, FuncType) and
            (self.ret_type is not None and self.ret_type.subsumes(other.ret_type)) and
            len(other.arg_types) == len(self.arg_types) and
            all(a is not None and a.subsumes(b) for a, b in zip(self.arg_types, other.arg_types))
        )

    def ll_type(self):
        args = [ a.ll_type() for a in self.arg_types ]
        return ll.FunctionType(self.ret_type.ll_type(), args)


class FuncDefArg:
    def __init__(self, name, index:int=None, dtype:Type=None, is_list:bool=False, is_dict:bool=False, default_val=None):
        self.name = name
        self.index = index
        self.default_val = default_val
        self.dtype = dtype
        self.is_list = is_list
        self.is_dict = is_dict

    def __repr__(self):
        return f'FuncDefArg({self.name}, idx={self.index}, type={repr(self.dtype)}, default={repr(self.default_val)})'

    def before_ll_ast(self):
        pass

    def clone(self):
        return copy.deepcopy(self)

    def cpp_name(self):
        return f'_func_arg_{self.name}_{self.index}'

    def bind_to_args(self, args:OrderedDict, matched:OrderedDict):
        arg_by_index = args.get(self.index)
        arg_by_name = args.get(self.name) if self.name else None
        uses_default_value = False
        desc = self.name or self.index

        if arg_by_index and arg_by_name:
            raise DuplicateParamError(f"Function parameter {desc} specified twice.")

        if not arg_by_index and not arg_by_name:
            if not self.default_val:
                raise MissingParamError(f"Missing function parameter {desc}.")

            # Otherwise, unmatched param, use default value
            uses_default_value = True

        if self.index in matched or self.name in matched:
            raise DuplicateParamError(f"Function parameter {desc} specified twice.")

        # Store the match, no other param can match to this arg
        arg = arg_by_index or arg_by_name
        matched[self.index] = (self, arg, uses_default_value)
        if self.name:
            matched[self.name] = (self, arg, uses_default_value)


class FuncDef(VarScope):
    clone_attrs = [ 'is_cls_inst_method' ]

    def __init__(self, func_args=None, is_cls_inst_method=False, **kwargs):
        super().__init__(**kwargs)
        self.func_args:List[FuncDefArg] = func_args or []
        for i, arg in enumerate(self.func_args):
            arg.index = i
        self.return_nodes = []
        # "template discovery" vs "instance build" mode
        self.build_as_instance = False
        self.is_built_inst = False
        self.is_built_def = False
        self.did_define_var = False

        self.is_cls_inst_method = is_cls_inst_method

    def __repr__(self):
        args = ', '.join(repr(arg) for arg in self.func_args)
        return f'FuncDef({self.name}, [{args}])'

    def get_local_symbol(self, name):
        if name == 'me':
            return self.cls_inst
        return super().get_local_symbol(name)

    def put_scoped_var(self, var):
        if var.name == 'me':
            raise ReservedSymbolError()

    def clone(self):
        clone = super().clone()
        clone.func_args = [ arg.clone() for arg in self.func_args ]

        for ret in self.return_nodes:
            path = self.get_path_to_node(ret)
            clone.return_nodes.append(clone.get_node_at_path(path))

        return clone

    def before_build(self):
        super().before_build()

        self.return_nodes = []

        for arg in self.func_args:
            self.put_scoped_var(FuncParamVariable(arg))

    def build_inner(self):
        if not self.return_nodes:
            ret = ReturnStmt()   # return void
            ret.parent = self
            self.children.append(ret)
            self.set_rebuild()
            return   # rebuild

    def after_build(self):
        # Don't declare variable to module scope if this is instantiation,
        # only declare during template discovery phase
        if self.build_as_instance:
            return

        scope = self.get_enclosing_scope()
        existing = scope.get_scoped_var(self.name)
        if not existing:
            scope.put_scoped_var(self)

        elif isinstance(existing, FuncDef):
            overload = FuncOverload(name=self.name)
            overload.add_overload(existing)
            overload.add_overload(self)
            scope.put_scoped_var(overload)

        elif isinstance(existing, FuncOverload):
            existing.add_overload(self)

    def solve_ret_type(self):
        assert self.return_nodes

        if len(self.return_nodes) == 1:
            return self.return_nodes[0].type

        else:
            ret_type = self.return_nodes[0]
            for node in self.return_nodes[1:]:
                ret_type = UnionType.make_union(ret_type, node.type)

    def bind_args(self, bind_args:OrderedDict):
        num_args_no_default = sum(int(not arg.default_val) for arg in self.func_args)
        if len(bind_args) < num_args_no_default:
            raise InvokeArgCountError(f"Function {self.name} requires at least {num_args_no_default} args, "
                                      f"but was called with {len(bind_args)}")

        matched = OrderedDict()
        for arg in self.func_args:
            arg.bind_to_args(bind_args, matched)

        unbound = [ str(key) for key in bind_args.keys() if key not in matched ]
        if unbound:
            names = ', '.join(unbound)
            raise UnusedParamError(f"Function {self.name} failed to bind params: {names}")

        positional_args = [ match for key, match in matched.items() if isinstance(key, int) ]

        bind_args = [ FuncBindArg(index=arg.index, invoke_arg=invoke_arg, bind_to_arg=func_arg, use_default=use_default)
                      for func_arg, invoke_arg, use_default in positional_args ]

        bind_args.sort(key=lambda arg: arg.index)

        binding = FuncBind(func_def=self, ret_type=self.solve_ret_type(), bind_args=bind_args)

        binding.verify_predictates()

        return binding

    def to_ll_ast(self):
        return { "op": "pass", "comment": "FuncDef" }

    def to_cpp(self, b):
        pass


class ReturnStmt(Node):
    def build_inner(self):
        func = self.get_enclosing_func()
        func.return_nodes.append(self)

        if len(self.children) == 0:
            self.type = VoidType()
        elif len(self.children) == 1:
            self.type = self.children[0].type
        else:
            raise Exception("ReturnStmt must have 0 or 1 children.")

    def to_ll_ast(self):
        if self.children:
            return { 'op': 'ret', 'value': self.children[0].to_ll_ast() }

        return { 'op': 'ret_void' }

    def to_cpp(self, b):
        b.c.emit('return ')
        if self.children:
            self.children[0].to_cpp(b)


class FuncBindArg:
    def __init__(self, index, invoke_arg:"InvokeArg", bind_to_arg:FuncDefArg, use_default:bool):
        self.index = index
        self.invoke_arg = invoke_arg
        self.bind_to_arg = bind_to_arg
        self.use_default = use_default

    def clone(self):
        return copy.deepcopy(self)

    def before_ll_ast(self):
        self.bind_to_arg.before_ll_ast()
        if self.invoke_arg:
            self.invoke_arg.before_ll_ast()

    def ll_type(self):
        return self.get_arg_type().ll_type()

    def cpp_type(self):
        return self.get_arg_type().cpp_type()

    def cpp_name(self):
        return self.bind_to_arg.cpp_name()

    def get_arg_type(self):
        # If a param uses default value (e.g. foo(x=3)), bind to that type
        if self.use_default:
            return self.bind_to_arg.default_val.type
        # Otherwise, use the type of parameter that was passed
        else:
            return self.invoke_arg.value.type

    def get_type_name(self):
        if self.use_default:
            return self.bind_to_arg.default_val.type.shortname()
        else:
            return self.invoke_arg.get_type_name()

    def to_ll_ast(self):
        # If default param, just build the LL AST of the default param value
        if self.use_default:
            return self.bind_to_arg.default_val.to_ll_ast()
        # Otherwise, func arg is a passed value, build llast for that node
        else:
            return self.invoke_arg.to_ll_ast()

class FuncBind:
    def __init__(self, func_def:FuncDef, ret_type:Type, bind_args:List[FuncBindArg], requires_cast:bool = False):
        self.func_def = func_def
        self.bind_args = [ arg.clone() for arg in bind_args ]
        self.ret_type = ret_type
        self.requires_cast = requires_cast

    def clone(self):
        return FuncBind(
            func_def=self.func_def.clone(),
            ret_type = self.ret_type,
            bind_args = [ arg.clone() for arg in self.bind_args ],
            requires_cast = self.requires_cast)

    def get_type_name(self):
        """Return a unique name based on the bound function signature."""
        name = self.func_def.name
        name = f"{name}_{self.ret_type.shortname()}"
        arg_str = '_'.join(arg.get_type_name() for arg in self.bind_args)
        if arg_str:
            name = f"{name}_{arg_str}"
        return name

    def verify_predictates(self):
        """Check to make sure all types and conditional predicates of each parameter
        match the function signature."""

        self.requires_cast = False

        for arg in self.bind_args:
            ltype = arg.bind_to_arg.dtype
            if arg.use_default:
                arg_val = arg.bind_to_arg.default_val
            else:
                arg_val = arg.invoke_arg.value
            rtype = arg_val.type
            cast = None

            if ltype is None or rtype.equivalent(ltype):
                continue

            elif ltype.subsumes(rtype):
                cast = SubsumeType(type=ltype, children=[ arg_val ], parent=arg_val.parent)

            elif rtype.can_cast_to(ltype):
                cast_op = rtype.get_cast_op(ltype)
                cast = CastType(type=ltype, children=[ arg_val ], cast_op=cast_op, parent=arg_val.parent)

            else:
                raise InvalidOverloadError(f"Parameter {arg.name} of type {ltype} does not overload to type {rtype}")

            if cast is not None:
                self.requires_cast = True
                arg.invoke_arg.value = cast


class FuncInst(BindInst):
    def __init__(self, name:str, func_def:FuncDef, func_bind:FuncBind, parent):
        super().__init__(name=name, parent=parent)

        # Keep a copy of the function definition
        self.func_def = func_def.clone()
        self.func_def.parent = self
        self.func_def.build_as_instance = True

        self.func_bind = func_bind
        self.func_ptr_id = next_id()
        self.is_built = False

    def find_type_up(self, dtype, search_self):
        if self.parent and dtype is type(self.parent):
            return self.parent
        else:
            return None

    def build(self):
        if not self.is_built:
            self.build_inner()
            self.is_built = True

    def build_inner(self):
        for func_arg, bind_arg in zip(self.func_def.func_args, self.func_bind.bind_args):
            func_arg.dtype = bind_arg.get_arg_type()

        self.func_def.build()

    def to_ll_ast(self):
        self.build()

        for arg in self.func_bind.bind_args:
            arg.before_ll_ast()

        for node in self.func_def.children:
            node.before_ll_ast()

        ll_args = [ { "type": arg.ll_type() } for arg in self.func_bind.bind_args ]

        return {
            "name": self.name,
            "args": ll_args,
            "id": self.func_ptr_id,
            "ret": { "type": self.func_bind.ret_type.ll_type() },
            "instrs": [ node.to_ll_ast() for node in self.func_def.children ]
        }

    def cpp_name(self):
        name = f'{self.name}_{self.func_ptr_id}'
        return re.sub(r'\W', '_', name)

    def to_cpp(self, b):
        ret = self.func_bind.ret_type.cpp_type()
        name = self.cpp_name()

        args = ', '.join([ f'{arg.cpp_type()} {arg.cpp_name()}'
                           for arg in self.func_bind.bind_args ])

        b.h.emit(f'\n{ret} {name}({args});\n')

        b.c.emit(f'{ret} {name} ({args}) {{\n')

        with b.c.with_indent():
            for child in self.func_def.children:
                child.to_cpp(b)
                b.c.emit(';\n')

        b.c.emit('}\n\n')


class FuncOverload(Node):
    clone_attrs = [ 'name', 'overloads' ]

    def __init__(self, name=None, overloads=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.overloads:List[FuncDef] = overloads or []

    def is_overload_conflict(self, fd1:FuncDef, fd2:FuncDef):
        if len(fd1.func_args) != len(fd2.func_args):
            return False

        for arg1, arg2 in zip(fd1.func_args, fd2.func_args):
            if arg1.dtype != arg2.dtype:
                return False

        return True

    def add_overload(self, func_def:FuncDef):
        for func_def2 in self.overloads:
            if self.is_overload_conflict(func_def, func_def2):
                raise FuncOverloadConflictError(f"Function {func_def.name} has conflicting overloads.")

        self.overloads.append(func_def)

    def get_overload_bind(self, func_args:OrderedDict, func_def:FuncDef):
        if len(func_def.func_args) != len(func_args):
            return None   # can't bind mismatch arg count

        try:
            binding = func_def.bind_args(func_args)
        except:
            return None  # didn't bind arg names / types

        return { 'func_def': func_def, 'binding': binding }

    def get_matching_overload(self, func_args:OrderedDict):
        # Bind to the first possible function in the list of overloads
        matches = [ self.get_overload_bind(func_args, func_def) for func_def in self.overloads ]
        matches = [ m for m in matches if m is not None ]

        if len(matches) == 0:
            return None

        # If only matched a single definition, use it
        if len(matches) == 1:
            return matches[0]['func_def']

        # we matched several definitions, did one match without casting?
        non_casting = [ m for m in matches if not m['binding'].requires_cast ]
        if len(non_casting) == 1:
            return non_casting[0]['func_def']

        raise AmbiguousOverloadError(f"Matched multiple overloads to function {self.name}")


class InvokeFunc(Node):
    def __init__(self, func_inst:FuncInst, func_bind:FuncBind, **kwargs):
        super().__init__(**kwargs)
        self.func_inst = func_inst
        self.func_bind = func_bind

    def clone(self):
        clone = super().clone()
        clone.func_inst = self.func_inst
        clone.func_bind = self.func_bind.clone()
        return clone

    def build_inner(self):
        self.type = self.func_bind.ret_type

    def to_ll_ast(self):
        func_ptr = { 'id': self.func_inst.func_ptr_id }
        func_args = [ arg.to_ll_ast() for arg in self.func_bind.bind_args ]
        return { 'op': 'call', 'func': func_ptr, 'args': func_args }

    def to_cpp(self, b):
        name = self.func_inst.cpp_name()
        b.c.emit(f'{name}(')
        for i, arg in enumerate(self.func_bind.bind_args):
            if i > 0:
                b.c.emit(',')
            if arg.use_default:
                arg.bind_to_arg.default_val.to_cpp(b)
            else:
                arg.invoke_arg.to_cpp(b)
        b.c.emit(')')



class Invoke(Node):
    """Generic invocation of an object / function in drake."""
    def build_inner(self):
        symbol = self.children[0]

        if isinstance(symbol, FuncDef):
            self.invoke_as_func(symbol)

        elif isinstance(symbol, GetAttr):
            func_def = symbol.inst_method
            if isinstance(func_def, FuncDef):
                self.invoke_as_func(func_def)
            elif isinstance(func_def, FuncOverload):
                self.invoke_as_overload(func_def)

        elif isinstance(symbol.var, FuncDef):
            self.invoke_as_func(symbol.var)

        elif isinstance(symbol.var, FuncOverload):
            self.invoke_as_overload(symbol.var)

        elif isinstance(symbol.var, ClassDef):
            self.invoke_as_class_def(symbol.var)

    def invoke_as_func(self, func_def:FuncDef, args_dict:OrderedDict=None):
        if args_dict is None:
            args_dict = self.args_to_dict()
        func_bind = func_def.bind_args(args_dict)
        func_inst = self.get_enclosing_scope().get_func_instance(func_def, func_bind)
        self.parent.replace_child(self, InvokeFunc(func_inst, func_bind))

    def invoke_as_overload(self, func_ovr:FuncOverload):
        args_dict = self.args_to_dict()
        func_def = func_ovr.get_matching_overload(args_dict)
        if not func_def:
            # TODO: print full attempted arg signature here
            raise InvalidOverloadError(f"Could not match overload for function {func_ovr.name}")

        self.invoke_as_func(func_def, args_dict)

    def invoke_as_class_def(self, class_def:ClassDef):
        # We know arg[0] is ClassDef, keep all other args for ctor invoke
        ctor_args = [ child.clone() for child in self.children[1:] ]

        alloc_stmt = AllocClassInst(children=[
            ClassInst(class_def=class_def),
            CtorArgs(children=ctor_args)
        ])

        # No longer need this invocation, replace with reference
        # to read pointer in the temp var
        self.parent.replace_child(self, alloc_stmt)


    def args_to_dict(self) -> OrderedDict:
        args = self.children[1:]
        arg_dict = OrderedDict()
        for i, arg in enumerate(args):
            key = arg.name or i
            arg_dict[key] = arg
        return arg_dict


class InvokeArg(Node):
    clone_attrs = [ 'name', 'index', 'value' ]

    def __init__(self, name=None, index=None, value=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.index = index
        self.value = value

    def shift_index(self, count):
        if self.index is not None:
            self.index += count

    def before_ll_ast(self):
        super().before_ll_ast()
        self.value.before_ll_ast()

    def build_inner(self):
        if not self.value:
            return

        self.value.parent = self.parent
        self.value.build()
        self.type = self.value.type

        # Does our arg refer to a variable?  If so, pass that to the function, instead of a ref name.
        if hasattr(self.value, 'var'):
            self.type = self.value.var.type
            self.value = self.value.var


    def get_type_name(self):
        return self.value.type.shortname()

    def to_ll_ast(self):
        return self.value.to_ll_ast()

    def to_cpp(self, b):
        self.value.to_cpp(b)
