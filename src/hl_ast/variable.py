from src.exceptions import *
from src.llvm_ast import next_id
from .node import Node
from ..warnings import Warnings
from .union import UnionType


class Variable:
    clone_attrs = [ 'name', 'value', 'fixed_type' ]

    def __init__(self, name, value=None, type=None, fixed_type:bool=False):
        self.name = name
        self.value = value
        self.ll_id = next_id()
        self.type = type
        # Can we change the type, or is it user specified / fixed?
        self.fixed_type = fixed_type

    def ll_ref(self):
        if not self.type:
            raise UnknownTypeError(f"Variable {self.name} has undefined type.")

        return { "type": self.type.ll_type(), "id": self.ll_id, "name": self.name }


class DefVar(Node):
    clone_attrs = [ 'name', 'implicit' ]

    def __init__(self, name, implicit:bool=False, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.implicit = implicit

    def build_inner(self):
        self.var = Variable(self.name, type=self.type)
        scope = self.get_enclosing_scope()
        existing = scope.get_scoped_var(self.var, local_only=True)

        # If we already have a variable by this name, could be error.
        # If this is "implicit" then we don't warn, since compiler generated the instruction.
        if existing and not self.implicit:
            Warnings.emit(Warnings.duplicate_var, f"Variable {self.name} was already declared in this scope.")

        scope.put_scoped_var(self.var)

    def to_ll_ast(self):
        # TODO: handle classes and malloc here based on type
        return { "op": "alloca", "ref": self.var.ll_ref() }


class BareName(Node):
    clone_attrs = [ 'name' ]

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.var:Variable = None

    def build_inner(self):
        self.var = self.get_locals().get(self.name)
        if not self.var:
            raise UndefinedVariableError(f'Undefined symbol {self.name}')

        # If variable is function param, ast can refer directly to function param
        if isinstance(self.var, FuncParamVariable):
            self.parent.replace_child(self, self.var)

    def to_ll_ast(self):
        if self.is_rvalue():
            return { "op": "load", "ref": self.var.ll_ref() }
        elif self.is_lvalue():
            return self.var.ll_ref()


class FuncParamVariable(Node):
    def __init__(self, func_arg=None, **kwargs):
        super().__init__(**kwargs)
        self.func_arg = func_arg
        if func_arg:
            self.type = func_arg.dtype

    @property
    def name(self):
        return self.func_arg.name

    def clone(self):
        clone = super().clone()
        clone.func_arg = self.func_arg.clone()
        return clone

    def to_ll_ast(self):
        return { "op": "func_arg", "value": self.func_arg.index }