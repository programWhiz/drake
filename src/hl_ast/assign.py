from .var_scope import VarScope
from .variable import Variable, DefVar, BareName
from .cast import SubsumeType, CastType
from .class_def import ClassInst, GetAttr, SetAttr
from .binary_op import BinaryOp


class Assign(BinaryOp):
    def build_inner(self):
        left, right = self.children[0:2]

        # If we are assigning to a class field, use SetAttr instead
        if isinstance(left, GetAttr):
            return self.parent.replace_child(self, [
                SetAttr(children=[ left, right ])
            ])

        scope:VarScope = self.get_enclosing_scope()

        existing:Variable = scope.get_scoped_var(left.var)
        if existing is None:
            scope.put_scoped_var(left.var.name)
        else:
            left.var = existing

        # If referencing a variable by name, get the variable
        if isinstance(right, BareName):
            right = right.var

        # TODO: actually figure out assign in condition
        ltype = left.var.type
        rtype = right if isinstance(right, ClassInst) else right.type

        # If left is same as right type, can always assign
        if ltype is None or ltype.equivalent(rtype):
            left.var.type = rtype
            self.type = rtype

            # Refer to the class inst itself if constructed on RHS
            left.var.value = right

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
        left, right = self.children
        return {
            'op': 'store',
            'ref': left.to_ll_ast(),
            'value': right.to_ll_ast(),
            "comment": "Assign" }
