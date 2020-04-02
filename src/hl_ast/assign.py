from .variable import DefVar, BareName
from .cast import SubsumeType, CastType
from .class_def import ClassInst, GetAttr, SetAttr
from .binary_op import BinaryOp
from src.exceptions import *
from .union import UnionType
import llvmlite.ir as ll


class Assign(BinaryOp):
    clone_attrs = [ 'assign_union' ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.assign_union = False

    def build_inner(self):
        left, right = self.children[0:2]

        # If we are assigning to a class field, use SetAttr instead
        if isinstance(left, GetAttr):
            return self.parent.replace_child(self, [
                SetAttr(children=[ left, right ])
            ])

        if not hasattr(left, 'var'):
            raise InvalidAssignError(f"Cannot assign to non-variable type {left.type}")

        # If referencing a variable by name, get the variable
        if isinstance(right, BareName):
            right = right.var

        # TODO: actually figure out assign in condition
        ltype = left.var.type
        rtype = right if isinstance(right, ClassInst) else right.type

        # If left is same as right type, can always assign
        if ltype is None or ltype.equivalent(rtype):
            if ltype is None:
                left.var.type = rtype
                self.type = rtype
            else:
                self.type = ltype

            # Refer to the class inst itself if constructed on RHS
            left.var.value = right
            return

        # If the left is fixed type, can we adjust right to match it?
        elif left.var.fixed_type:
            if ltype.subsumes(rtype):
                new_right = SubsumeType(type=ltype, children=[ right ])
            elif rtype.can_cast_to(ltype):
                cast_op = rtype.get_cast_op(ltype)
                new_right = CastType(type=ltype, children=[right], cast_op=cast_op)
            # Can't subsume or cast the right type
            else:
                raise InvalidTypeError(f"Cannot assign value of type {rtype} to required type {ltype}")

            self.type = ltype
            self.replace_child(right, new_right)

        else:  # left is not fixed type, just overwrite var with new type
            self.type = rtype
            self.replace_child(left, DefVar(left.var.name, implicit=True, type=rtype, parent=self))

    def to_cpp(self, b):
        self.children[0].to_cpp(b)
        b.c.emit(' = ')
        self.children[1].to_cpp(b)

    def to_ll_ast(self):
        left, right = self.children

        if isinstance(left.type, UnionType):
            return self.store_union_ll_ast()

        return {
            'op': 'store',
            'ref': left.to_ll_ast(),
            'value': right.to_ll_ast(),
            "comment": "Assign" }

    def store_union_ll_ast(self):
        left, right = self.children
        union = left.type
        type_idx = union.get_type_index(right.type)

        store_type = {
            "op": "store",
            "ref": {
                "op": "gep",
                "ref": left.ll_ref(),
                "value": [ 0, 0 ]
            },
            "value": {
                "op": "const_val",
                "value": ll.Constant(ll.IntType(8), type_idx)
            }
        }

        value_ptr = {
            "op": "gep",
            "ref": left.ll_ref(),
            "value": [0, 1]
        }

        store_ptr = {
            "op": "store",
            "ref": {
                "op": "cast_ptr",
                "ref": value_ptr,
                "type": right.ll_type()
            },
            "value": right.to_ll_ast()
        }

        return {
            "op": "instr_list",
            "instrs": [ store_type, store_ptr ]
        }

    def is_child_lvalue(self, child):
        return child == self.children[0]

    def is_child_rvalue(self, child):
        return child == self.children[1]

