from .node import Node


class BinaryOp(Node):
    def is_child_lvalue(self, child):
        return False

    def is_child_rvalue(self, child):
        return True


