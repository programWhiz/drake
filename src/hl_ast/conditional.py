from collections import Counter
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
        # Gather up the list of variable names, and their respective assignment
        # statements in each branch.  Due to Dict nature, only the last assignment
        # of each variable in each branch is in the list.
        branch_asmts:List[Dict[str, Assign]] = []
        for child in self.children[1:]:
            asmts = child.find_children_with_class(Assign)
            asmts = { ass.children[0].var.name: ass for ass in asmts }
            branch_asmts.append(asmts)

        if not any(branch_asmts):
            return  # early exit

        # Track how many branches each assignment is in
        assign_counts = Counter()
        for asmt in branch_asmts:
            assign_counts.update(asmt.keys())

        # Keep only assignments that are present in at least two branches
        common_names = [ key for key, count in assign_counts.items() if count >= 2 ]
        if not common_names:
            return   # early exit

        for varname, count in assign_counts.items():
            if count < 2:
                for asmt in branch_asmts:
                    asmt.pop(varname)

        create_unions = []
        for name in common_names:
            all_asmts = [ asmt[name] for asmt in branch_asmts if asmt.get(name) ]

            union = None
            for asmt in all_asmts:
                union = UnionType.make_union(union, asmt.type)
            union.is_fixed = True

            # If any of the branches would change type, create the union before all branches
            if any(not asmt.type.equivalent(union) for asmt in all_asmts):
                create_unions.append((name, union))

        # Will only rebuild if some of the statements changed types
        for (name, union) in create_unions:
            def_var = DefVar(name, implicit=True, type=union, fixed_type=True)
            self.parent.insert_instrs_before(self, [ def_var ])

            self.get_enclosing_module().register_union_type(union)

        if create_unions:
            self.recursive_rebuild()

    def force_cond_to_bool(self, cond):
        if isinstance(cond.type, NumericType):
            # Cast non-boolean numerics by comparing with zero type
            if not cond.type.is_bool:
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

