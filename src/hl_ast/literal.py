import json
from .node import Node
import llvmlite.ir as ll
from .numeric import BoolType


class Literal(Node):
    clone_attrs = [ 'value' ]

    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def build_inner(self):
        pass

    def __repr__(self):
        return f'Literal({self.value})'

    def to_ll_ast(self):
        ll_type = self.type.ll_type()
        return { "op": "const_val",
                 "type": ll_type,
                 "value": ll.Constant(ll_type, self.value) }

    def to_cpp(self, b):
        if isinstance(self.type, BoolType):
            b.c.emit('true' if self.value else 'false')
        else:
            b.c.emit(json.dumps(self.value))


class StrLiteral(Literal):
    def __repr__(self):
        return f'StrLiteral("{self.value}")'

    def to_ll_ast(self):
        return { 'op': 'const_str', 'value': self.value }
