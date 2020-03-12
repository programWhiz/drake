import copy
from typing import List
from collections import OrderedDict
from .variable import Variable, BareName, FuncParamVariable
from .node import Node
from .var_scope import VarScope
from .type import Type, VoidType
from .union import UnionType
import llvmlite.ir as ll
from src.exceptions import *
from ..llvm_ast import next_id


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

    def clone(self):
        return copy.deepcopy(self)

    def bind_to_args(self, args:OrderedDict, matched:OrderedDict):
        arg_by_index = args.get(self.index)
        arg_by_name = args.get(self.name) if self.name else None
        desc = self.name or self.index

        if arg_by_index and arg_by_name:
            raise DuplicateParamError(f"Function parameter {desc} specified twice.")

        if not arg_by_index and not arg_by_name:
            raise MissingParamError(f"Missing function parameter {desc}.")

        if self.index in matched or self.name in matched:
            raise DuplicateParamError(f"Function parameter {desc} specified twice.")

        # Store the match, no other param can match to this arg
        arg = arg_by_index or arg_by_name
        matched[self.index] = (self, arg)
        if self.name:
            matched[self.name] = (self, arg)


class FuncDef(VarScope):
    def __init__(self, func_args=None, **kwargs):
        super().__init__(**kwargs)
        self.func_args:List[FuncDefArg] = func_args or []
        for i, arg in enumerate(self.func_args):
            arg.index = i
        self.return_nodes = []
        # "template discovery" vs "instance build" mode
        self.build_as_instance = False

    def clone(self):
        clone = super().clone()
        clone.func_args = [ arg.clone() for arg in self.func_args ]
        return clone

    def before_build(self):
        super().before_build()

        self.return_nodes = []

        for arg in self.func_args:
            self.put_scoped_var(FuncParamVariable(arg))

    def build_inner(self):
        # Don't form template in "instance mode", only in "template mode"
        if not self.build_as_instance:
            module = self.get_enclosing_module()
            module.func_tpls[self.name] = self

        if not self.return_nodes:
            ret = ReturnStmt()   # return void
            ret.parent = self
            self.children.append(ret)
            self.set_rebuild()
            return   # rebuild

    def after_build(self):
        # Don't declare variable to module scope if this is instantiation,
        # only declare during template discovery phase
        if not self.build_as_instance:
            self.get_enclosing_scope().put_scoped_var(self)

    def solve_ret_type(self):
        assert self.return_nodes

        if len(self.return_nodes) == 1:
            return self.return_nodes[0].type

        else:
            ret_type = self.return_nodes[0]
            for node in self.return_nodes[1:]:
                ret_type = UnionType.make_union(ret_type, node.type)

    def bind_args(self, bind_args:OrderedDict):
        if len(bind_args) != len(self.func_args):
            raise InvokeArgCountError(f"Function {self.name} expects {len(self.func_args)} args, but was called with {len(bind_args)}")

        matched = OrderedDict()
        for arg in self.func_args:
            arg.bind_to_args(bind_args, matched)

        unbound = [ str(key) for key in bind_args.keys() if key not in matched ]
        if unbound:
            names = ', '.join(unbound)
            raise UnusedParamError(f"Function {self.name} failed to bind params: {names}")

        positional_args = [ match for key, match in matched.items() if isinstance(key, int) ]

        bind_args = [ FuncBindArg(index=arg.index, invoke_arg=invoke_arg, bind_to_arg=func_arg)
                      for func_arg, invoke_arg in positional_args ]

        bind_args.sort(key=lambda arg: arg.index)

        binding = FuncBind(func_def=self, ret_type=self.solve_ret_type(), bind_args=bind_args)

        return binding

    def to_ll_ast(self):
        return { 'op': 'pass' }


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


class FuncBindArg:
    def __init__(self, index, invoke_arg:"InvokeArg", bind_to_arg:FuncDefArg):
        self.index = index
        self.invoke_arg = invoke_arg
        self.bind_to_arg = bind_to_arg

    def clone(self):
        return copy.deepcopy(self)


class FuncBind:
    def __init__(self, func_def:FuncDef, ret_type:Type, bind_args:List[FuncBindArg]):
        self.func_def = func_def
        self.bind_args = bind_args
        self.ret_type = ret_type

    def clone(self):
        return FuncBind(
            func_def=self.func_def.clone(),
            ret_type = self.ret_type,
            bind_args = [ arg.clone() for arg in self.bind_args ])

    def get_type_name(self):
        name = self.func_def.name
        name = f"{name}_{self.ret_type.shortname()}"
        arg_str = '_'.join(arg.invoke_arg.get_type_name() for arg in self.bind_args)
        if arg_str:
            name = f"{name}_{arg_str}"
        return name


class FuncInst:
    def __init__(self, name:str, func_def:FuncDef, func_bind:FuncBind, module):
        # Only keep a copy of the function definition we are free to modify
        self.name = name

        self.module = module

        self.func_def = func_def.clone()
        self.func_def.parent = self
        self.func_def.build_as_instance = True

        self.func_bind = func_bind
        self.func_ptr_id = next_id()
        self.is_built = False

    def find_type_up(self, type, search_self):
        from .module import Module
        if type is Module:
            return self.module
        else:
            raise Exception("FuncInst only parented by module scope.")

    def build(self):
        if not self.is_built:
            self.build_inner()
            self.is_built = True

    def build_inner(self):
        for i, arg in enumerate(self.func_def.func_args):
            arg.dtype = self.func_bind.bind_args[i].invoke_arg.value.type

        self.func_def.build()

    def to_ll_ast(self):
        self.build()

        return {
            "name": self.name,
            "args": [ { "type": arg.invoke_arg.value.type.ll_type() } for arg in self.func_bind.bind_args ],
            "id": self.func_ptr_id,
            "ret": { "type": self.func_bind.ret_type.ll_type() },
            "instrs": [ node.to_ll_ast() for node in self.func_def.children ]
        }


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
        func_args = [ arg.invoke_arg.to_ll_ast() for arg in self.func_bind.bind_args ]
        return { 'op': 'call', 'func': func_ptr, 'args': func_args }


class Invoke(Node):
    """Generic invocation of an object / function in drake."""
    def build_inner(self):
        symbol = self.children[0]
        args_dict = self.args_to_dict()

        if isinstance(symbol.var, FuncDef):
            func_def = symbol.var
            func_bind = func_def.bind_args(args_dict)
            func_inst = self.get_enclosing_scope().get_func_instance(func_def, func_bind)
            self.parent.replace_child(self, InvokeFunc(func_inst, func_bind))

    def args_to_dict(self):
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

    def get_type_name(self):
        return self.value.type.shortname()

    def to_ll_ast(self):
        return self.value.to_ll_ast()
