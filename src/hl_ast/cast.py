from .node import Node
from .union import UnionType


class SubsumeType(Node):
    clone_attrs = [ 'type_idx' ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_idx = -1

    def build_inner(self):
        right = self.children[0]
        union:UnionType = self.type
        self.type_idx = union.get_type_index(right.type)

    def to_ll_ast(self):
        return self.children[0].to_ll_ast()


class CastType(Node):
    clone_attrs = [ 'cast_op' ]

    def __init__(self, cast_op=None, **kwargs):
        super().__init__(**kwargs)
        self.cast_op = cast_op

    def to_ll_ast(self):
        return {
            "op": self.cast_op,
            "value": self.children[0].to_ll_ast(),
            "type": self.type.ll_type() }

    def to_cpp(self, b):
        b.c.emit(f"({self.type.cpp_type()})")
        self.children[0].to_cpp(b)
