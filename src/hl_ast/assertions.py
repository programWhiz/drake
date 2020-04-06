from .node import Node
from .if_else import IfStmt
from .con


class Assert(Node):
    def build_inner(self):
        self.parent.replace_child(self, [
            IfStmt(children=[

            ])
        ])
