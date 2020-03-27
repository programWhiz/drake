from .binary_op import BinaryOp
from .cast import CastType
from .func_def import Invoke
from .variable import BareName, Variable
from .numeric import BoolType


class ComparisonOp(BinaryOp):
    clone_attrs = [ 'op', 'overload', 'concrete_op' ]

    def __init__(self, op=None, overload=None, **kwargs):
        super().__init__(**kwargs)
        self.op = op
        self.concrete_op = None
        self.overload = overload
        self.type = BoolType()

    def build_inner(self):
        left, right = self.children
        ltype, rtype = left.type, right.type

        if ltype.is_primitive() and rtype.is_primitive():
            self.build_for_primitives(left, right, ltype, rtype)
        else:  # must use some overloaded operator e.g. "_gt_" or "_eq_"
            self.parent.replace_child(self, [
                Invoke(children=[
                    BareName(self.overload), left, right
                ])
            ])

    def cast_left_right_prims(self, left, right, ltype, rtype):
        if ltype.is_int == rtype.is_int:
            if rtype.can_cast_to(ltype):
                cast_op = rtype.get_cast_op(ltype)
                self.replace_child(right, CastType(type=ltype, children=[right], cast_op=cast_op))
            else:  # cast left
                cast_op = ltype.get_cast_op(rtype)
                self.replace_child(left, CastType(type=rtype, children=[left], cast_op=cast_op))
            return

        # One of the two is float
        cast_op = ltype.get_float_cast(rtype)
        if cast_op:
            self.replace_child(left, CastType(type=rtype, children=[left], cast_op=cast_op))
        else:
            cast_op = rtype.get_float_cast(ltype)
            self.replace_child(right, CastType(type=ltype, children=[right], cast_op=cast_op))

    def build_for_primitives(self, left, right, ltype, rtype):
        if not rtype.equivalent(ltype):
            self.cast_left_right_prims(left, right, ltype, rtype)
            return

        self.concrete_op = self.get_concrete_op(ltype)

    def get_concrete_op(self, dtype):
        if dtype.is_bool:
            prefix = 'u'  # bool always unsigned int
        elif dtype.is_int:  # signed or unsigned int
            prefix = 's' if dtype.signed_int else 'u'
        else:  # float
            prefix = 'f'

        return f'{prefix}{self.op}'

    def to_ll_ast(self):
        left, right = self.children

        return {
            'op': self.concrete_op,
            'left': left.to_ll_ast(),
            'right': right.to_ll_ast(),
        }


class GreaterThan(ComparisonOp):
    def __init__(self, **kwargs):
        super().__init__(op='>', overload='_gt_', **kwargs)


class GreaterThanEq(ComparisonOp):
    def __init__(self, **kwargs):
        super().__init__(op='>=', overload='_ge_', **kwargs)


class LessThan(ComparisonOp):
    def __init__(self, **kwargs):
        super().__init__(op='<', overload='_lt_', **kwargs)


class LessThanEq(ComparisonOp):
    def __init__(self, **kwargs):
        super().__init__(op='<=', overload='_le_', **kwargs)


class EqualTo(ComparisonOp):
    def __init__(self, **kwargs):
        super().__init__(op='==', overload='_eq_', **kwargs)


class NotEqualTo(ComparisonOp):
    def __init__(self, **kwargs):
        super().__init__(op='!=', overload='_ne_', **kwargs)
