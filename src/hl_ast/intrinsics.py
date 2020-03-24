from .node import Node
from .numeric import NumericType
from src.exceptions import *
from .cast import CastType
from .literal import StrLiteral


class CallIntrinsic(Node):
    clone_attrs = [ 'intrinsic' ]

    def __init__(self, intrinsic:str=None, **kwargs):
        super().__init__(**kwargs)
        self.intrinsic = intrinsic

    def to_ll_ast(self):
        args = [ child.to_ll_ast() for child in self.children ]
        return { "op": "call", "intrinsic": self.intrinsic, "args": args }


class Printf(CallIntrinsic):
    def __init__(self, **kwargs):
        kwargs['intrinsic'] = 'printf'
        super().__init__(**kwargs)


class Print(Node):
    def build_inner(self):
        fmts = [ self.get_format_str(child) for child in self.children ]
        self.fmt_str = ' '.join(fmts)
        self.fmt_str += '\n'

    def after_build(self):
        self.parent.replace_child(self, Printf(children=[
            StrLiteral(self.fmt_str), *self.children
        ]))

    def get_format_str(self, node):
        if isinstance(node.type, NumericType):
            return self.get_numeric_format(node)
        if isinstance(node, StrLiteral):
            return '%s'
        else:
            raise BuildException("No known print format for type: " + repr(node))

    def get_numeric_format(self, node):
        if node.type.is_int:
            return self.get_int_format(node)
        else:
            return self.get_float_format(node)

    def get_int_format(self, node):
        t = node.type

        # Minimum precision is 32, cast if necessary
        if t.precision < 32:
            cast = 'sext' if t.signed_int else 'zext'
            cast_node = CastType(cast, type=t.with_precision(32), children=[ node ])
            self.replace_child(node, cast_node)

        f = '%'
        if t.precision == 64:
            f += 'l'
        if t.precision == 128:
            f += 'll'
        f += 'd' if t.signed_int else 'u'
        return f

    def get_float_format(self, node):
        t = node.type
        if t.precision < 64:
            cast_node = CastType('fpext', type=t.with_precision(64), children=[ node ])
            self.replace_child(node, cast_node)
        return '%f'
