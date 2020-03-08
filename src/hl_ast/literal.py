from .node import Node
import llvmlite.ir as ll


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


