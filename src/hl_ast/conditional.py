from typing import List, Dict
from .node import Node
from .assign import Assign
from .union import UnionType, StackAllocUnion, UnionInst
from .variable import BareName, DefVar
from .numeric import NumericType
from .literal import Literal
from .comparison import NotEqualTo
from .func_def import Invoke, InvokeArg
from .instr_list import InstrList


class ConditionalStmt(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.did_assign_unions = False

    def is_conditional(self):
        return True

    def set_rebuild(self):
        super().set_rebuild()

    def assign_union_types(self):
        return
        true_asmts:List[Assign] = []
        self.children[1].find_children_with_class(Assign, out=true_asmts)

        false_asmts:List[Assign] = []
        self.children[2].find_children_with_class(Assign, out=false_asmts)

        # Keep the last assignment by name in both branches, keyed by name
        true_asmts:Dict[str, Assign] = { ass.children[0].var.name: ass for ass in true_asmts }
        false_asmts:Dict[str, Assign] = { ass.children[0].var.name: ass for ass in false_asmts }
        common_names = set(true_asmts.keys()) & set(false_asmts.keys())

        # Keep only common assignments from both branches
        true_asmts:Dict[str, Assign] = { name: ass for name, ass in true_asmts.items() if name in common_names }
        false_asmts:Dict[str, Assign] = { name: ass for name, ass in false_asmts.items() if name in common_names }

        do_rebuild = False
        for name, true_asmt in true_asmts.items():
            false_asmt = false_asmts[name]
            true_type, false_type = true_asmt.type, false_asmt.type
            # If both assigned types match, then we don't care, this
            # doesn't cause a conditional type difference
            if false_type.equivalent(true_type):
                continue

            # If types don't agree, then we must assign a Union type here
            union = UnionType.make_union(true_type, false_type)
            union.is_fixed = True

            # Now prior to both assignment instructions, insert the Union instruction
            for asmt in (true_asmt, false_asmt):
                if asmt.type.equivalent(union):
                    continue
                do_rebuild = True

                # Replace left variable type with new type
                lvalue = asmt.children[0]
                union_var = DefVar(name, implicit=True, type=union, fixed_type=True)
                asmt.replace_child(lvalue, union_var)

        if do_rebuild:
            self.recursive_rebuild()

    def force_cond_to_bool(self, cond):
        if isinstance(cond.type, NumericType):
            # Cast non-boolean numerics by comparing with zero type
            if not (cond.type.is_bool and cond.type.precision == 1):
                self.replace_child(cond, NotEqualTo(children=[
                    cond, Literal(0, type=cond.type)
                ]))
        else:  # evaluate as bool
            self.replace_child(cond, Invoke(children=[
                InvokeArg(index=0, value=BareName('_bool_')),
                InvokeArg(index=1, value=cond)
            ]))


    def force_node_to_instr_list(self, node):
        # Make sure body is made up of instruction lists, not single nodes
        if not isinstance(node, InstrList):
            self.replace_child(node, InstrList(children=[ node ]))

