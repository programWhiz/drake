from .node import Node


class BinaryOp(Node):
    def is_child_lvalue(self, child):
        return child == self.children[0]

    def is_child_rvalue(self, child):
        return child == self.children[1]


