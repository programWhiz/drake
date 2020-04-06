from .binary_op import BinaryOp
from .conditional import ConditionalStmt
from .numeric import BoolType


class BinaryLogicalOp(BinaryOp):
    def __init__(self, op=None, **kwargs):
        super().__init__(**kwargs)
        self.op = op
        self.type = BoolType()

    def build_inner(self):
        left, right = self.children
        ConditionalStmt.force_cond_to_bool(self, left)
        ConditionalStmt.force_cond_to_bool(self, right)

    def to_cpp(self, b):
        left, right = self.children
        b.c.emit('(')
        left.to_cpp(b)
        b.c.emit(f') {self.op} (')
        right.to_cpp(b)
        b.c.emit(')')


class UnaryLogicalOp(BinaryOp):
    def __init__(self, op=None, **kwargs):
        super().__init__(**kwargs)
        self.op = op
        self.type = BoolType()

    def build_inner(self):
        ConditionalStmt.force_cond_to_bool(self, self.children[0])

    def to_cpp(self, b):
        b.c.emit(f'{self.op} (')
        self.children[0].to_cpp(b)
        b.c.emit(')')


class LogicalAnd(BinaryLogicalOp):
    def __init__(self, **kwargs):
        super().__init__(op='&&', **kwargs)


class LogicalOr(BinaryLogicalOp):
    def __init__(self, **kwargs):
        super().__init__(op='||', **kwargs)


class LogicalXor(BinaryLogicalOp):
    def __init__(self, **kwargs):
        super().__init__(op='^', **kwargs)


class LogicalNot(UnaryLogicalOp):
    def __init__(self, **kwargs):
        super().__init__(op='!', **kwargs)
