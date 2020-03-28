from .node import Node
from .numeric import NumericType
from .literal import Literal
from .comparison import EqualTo
from .func_def import Invoke, InvokeArg
from .variable import BareName


class IfStmt(Node):
    def build_inner(self):
        cond = self.children[0]

        if isinstance(cond.type, NumericType):
            # Cast non-boolean numerics by comparing with zero type
            if not cond.type.is_bool:
                self.replace_child(cond, EqualTo(children=[
                    cond, Literal(0, dtype=cond.type)
                ]))
        else:  # evaluate as bool
            self.replace_child(cond, Invoke(children=[
                InvokeArg(index=0, value=BareName('_bool_')),
                InvokeArg(index=1, value=cond)
            ]))

    def to_ll_ast(self):
        cond, true_block, false_block = self.children

        return {
            "op": "if",
            "cond": cond.to_ll_ast(),
            "true": true_block.to_ll_ast(),
            "false": false_block.to_ll_ast(),
        }


class InstrList(Node):
    def to_ll_ast(self):
        return [ child.to_ll_ast() for child in self.children ]