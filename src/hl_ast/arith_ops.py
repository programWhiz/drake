from .comparison import ComparisonOp
from .binary_op import BinaryOp


class BinaryArithOp(ComparisonOp):
    clone_attrs = ['arith_op']

    def __init__(self, arith_op=None, **kwargs):
        super().__init__(**kwargs)
        self.arith_op = arith_op

    def get_concrete_op(self, dtype):
        self.type = dtype
        if not dtype.is_int:
            return f'f{self.arith_op}'
        return self.arith_op


class BinaryAdd(BinaryArithOp):
    def __init__(self, **kwargs):
        super().__init__(arith_op='add', **kwargs)


class BinarySub(BinaryArithOp):
    def __init__(self, **kwargs):
        super().__init__(arith_op='sub', **kwargs)


class BinaryMul(BinaryArithOp):
    def __init__(self, **kwargs):
        super().__init__(arith_op='mul', **kwargs)


class BinaryDiv(BinaryArithOp):
    def __init__(self, **kwargs):
        super().__init__(arith_op='div', **kwargs)

    def get_concrete_op(self, dtype):
        self.type = dtype
        if not dtype.is_int:
            return 'fdiv'
        elif dtype.signed_int:
            return 'sdiv'
        else:
            return 'udiv'
