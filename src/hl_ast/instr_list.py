from .node import Node
from .var_scope import insert_instrs_after_impl, insert_instrs_before_impl


class InstrList(Node):
    def to_ll_ast(self):
        return [ child.to_ll_ast() for child in self.children ]

    def insert_instrs_before(self, node, instrs):
        return insert_instrs_before_impl(self, node, instrs)

    def insert_instrs_after(self, node, instrs):
        return insert_instrs_after_impl(self, node, instrs)

    def to_cpp(self, b):
        for child in self.children:
            child.to_cpp(b)
            b.c.emit(';\n')
