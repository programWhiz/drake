from .var_scope import VarScope
from .node import Node
from .variable import Variable, DefVar
from .union import UnionType, GetUnionPointer
from .cast import SubsumeType, CastType


class BinaryOp(Node):
    def is_child_lvalue(self, child):
        return child == self.children[0]

    def is_child_rvalue(self, child):
        return child == self.children[1]


class Assign(BinaryOp):
    def build_inner(self):
        left, right = self.children[0:2]

        scope:VarScope = self.get_enclosing_scope()
        existing:Variable = scope.get_scoped_var(left.var)

        if existing is None:
            scope.put_scoped_var(left.var.name)
        else:
            left.var = existing

        # TODO: actually figure out assign in condition
        ltype = left.var.type
        rtype = right.type

        # If left is same as right type, can always assign
        if ltype is None or ltype.equivalent(rtype):
            left.var.type = rtype
            self.type = rtype

        # with unconditional assignment, if the left type isn't fixed, we
        # can just create a new reference of the desired type
        elif not left.var.fixed_type:
            # Implicitly declare a new variable replacing the old one
            left = DefVar(left.var.name, implicit=True, type=rtype, parent=self)
            self.set_rebuild()
            self.type = rtype
            self.children = [ left, right ]

        else:  # types don't match, but the assign is unconditional
            if ltype.subsumes(rtype):
                right = SubsumeType(type=ltype, children=[ right ])
            elif rtype.can_cast_to(ltype):
                cast_op = rtype.get_cast_op(ltype)
                right = CastType(type=ltype, children=[right], cast_op=cast_op)

            self.set_rebuild()
            self.type = ltype
            self.children = [ left, right ]
            left.parent, right.parent = self, self

        # TODO: handle non-variable?

    def to_ll_ast(self):
        left = self.children[0].to_ll_ast()
        right = self.children[1].to_ll_ast()

        return { 'op': 'store', 'ref': left, 'value': right }
