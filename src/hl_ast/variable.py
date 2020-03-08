from src.exceptions import *
from src.llvm_ast import next_id
from .node import Node
from ..warnings import Warnings
from .union import UnionType


class Variable:
    def __init__(self, name, value=None, type=None, fixed_type:bool=False):
        self.name = name
        self.ll_id = next_id()
        self.type = type
        # Can we change the type, or is it user specified / fixed?
        self.fixed_type = fixed_type

    def ll_ref(self):
        if not self.type:
            raise UnknownTypeError(f"Variable {self.name} has undefined type.")

        return { "type": self.type.ll_type(), "id": self.ll_id, "name": self.name }


class DefVar(Node):
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
