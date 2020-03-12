from .node import Node


class SubsumeType(Node):
    pass


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