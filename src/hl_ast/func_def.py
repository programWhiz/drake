from typing import List
from .node import Node
from .var_scope import VarScope
from .type import Type
import llvmlite.ir as ll


class FuncDefArg:
    def __init__(self, name, index, default_val, dtype):
        self.name = name
        self.index = index
        self.default_val = default_val
        self.dtype = dtype


class FuncDef(VarScope):
    def __init__(self, name:str, func_args=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.func_args:List[FuncDefArg] = func_args or []
        self.return_nodes = []

    def before_build(self):
        self.return_nodes = []

    def build_inner(self):
        module = self.get_enclosing_module()
        module.func_tpls[self.name] = self


class ReturnStmt(Node):
    def build_inner(self):
        func = self.get_enclosing_func()
        func.return_nodes.append(self)


class FuncBindArg:
    def __init__(self, key, index, value, bind_to_arg:FuncDefArg):
        self.key = key
        self.index = index
        self.value = value
        self.bind_to_arg = bind_to_arg


class FuncBind:
    def __init__(self, func_def:FuncDef, bind_args:list, bind_kwargs:dict):
        self.func_def = func_def
        self.bind_args = bind_args
        self.bind_kwargs = bind_kwargs


class InvokeFunc:
    def __init__(self, func_def:FuncDef, func_bind:FuncBind, ret_type:Type):
        self.func_def = func_def
        self.func_bind = func_bind
        self.ret_type = ret_type
