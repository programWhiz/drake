from .node import Node
from .conditional import ConditionalStmt


class IfStmt(ConditionalStmt):
    def build_inner(self):
        cond, true_block, false_block = self.children

        self.force_cond_to_bool(cond)
        self.force_node_to_instr_list(true_block)
        self.force_node_to_instr_list(false_block)

        if self.is_built:
            self.assign_union_types()

    def to_ll_ast(self):
        cond, true_block, false_block = self.children

        return {
            "op": "if",
            "cond": cond.to_ll_ast(),
            "true": true_block.to_ll_ast(),
            "false": false_block.to_ll_ast(),
        }

    def to_cpp(self, b):
        cond, true_block, false_block = self.children
        b.c.emit('if (')
        cond.to_cpp(b)
        b.c.emit(') {\n')

        with b.c.with_indent():
            true_block.to_cpp(b)

        b.c.emit('\n } else {\n')

        with b.c.with_indent():
            false_block.to_cpp(b)

        b.c.emit('}\n')


class Switch(Node):
    def build_inner(self):
        is_all_cases = all(isinstance(child, SwitchCase) for child in self.children)
        assert is_all_cases, "Switch only supports SwitchCase child."

    def to_ll_ast(self):
        return {
            "op": "switch",
            "comment": "Switch",
            "branch": [ child.to_ll_ast() for child in self.children ]
        }


class SwitchCase(ConditionalStmt):
    def build_inner(self):
        cond, body = self.children
        self.force_cond_to_bool(cond)

        if not isinstance(body, InstrList):
            self.replace_child(body, InstrList(children=[ body ]))

    def to_ll_ast(self):
        cond, body = self.children
        return {
            "comment": "SwitchCase",
            "cond": cond.to_ll_ast(),
            "instrs": body.to_ll_ast()
        }

