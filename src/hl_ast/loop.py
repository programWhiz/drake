from .node import Node
from .conditional import ConditionalStmt


class Loop(ConditionalStmt):
    def build_inner(self):
        cond, body = self.children
        self.force_cond_to_bool(cond)
        self.force_node_to_instr_list(body)

        if self.is_built:
            self.assign_union_types()

    def to_cpp(self, b):
        cond, body = self.children

        b.c.emit('while(')
        cond.to_cpp(b)
        b.c.emit('){\n')

        with b.c.with_indent():
            body.to_cpp(b)

        b.c.emit('}\n')
