from typing import List
from .type import Type


class Node:
    clone_attrs = [ 'type' ]
    unsolved_nodes = set()

    def __init__(self, parent=None, children=None, type:Type=None):
        self.parent:"Node" = parent
        self.children:List["Node"] = children or []
        for child in self.children:
            child.parent = self
        self.is_built = False
        self.type:Type = type
        # Set of nodes which must be solved before this node
        self.solve_depends = set()
        # Set of nodes to solve after this node
        self.solve_nodes = set()

    def mark_unsolved(self, depends_on_node):
        if isinstance(depends_on_node, (list, tuple, set)):
            depends_on_node = set(depends_on_node)
        if isinstance(depends_on_node, set):
            self.solve_depends |= depends_on_node
            Node.unsolved_nodes |= depends_on_node
        else:
            self.solve_depends.add(depends_on_node)
            Node.unsolved_nodes.add(depends_on_node)
        Node.unsolved_nodes.add(self)

    def is_unsolved(self):
        return len(self.solve_depends)

    def before_ll_ast(self):
        for child in self.children:
            child.before_ll_ast()

    def get_locals(self):
        return self.get_enclosing_scope().get_locals()

    def get_globals(self):
        return self.get_enclosing_scope().get_globals()

    def clone(self):
        cls = self.__class__
        clone_attrs = set(cls.clone_attrs)
        for sup_cls in cls.mro():
            clone_attrs |= set(getattr(sup_cls, 'clone_attrs', set()))

        kwargs = { attr: getattr(self, attr) for attr in clone_attrs }
        inst = cls(**kwargs)

        for child in self.children:
            clone = child.clone()
            clone.parent = inst
            inst.children.append(clone)

        return inst

    def replace_child(self, node, repl_nodes):
        if not repl_nodes:
            return self.remove(node)

        if isinstance(repl_nodes, Node):
            repl_nodes = [ repl_nodes ]

        index_of = self.children.index(node)
        self.children[index_of:index_of+1] = repl_nodes
        for node in repl_nodes:
            node.parent = self

        self.set_rebuild()

    def remove(self, node):
        self.children.remove(node)
        self.set_rebuild()

    def add(self, *nodes):
        if nodes:
            for node in nodes:
                node.parent = self
                self.children.append(node)

    def set_rebuild(self):
        self.is_built = False

    def recursive_rebuild(self):
        self.set_rebuild()
        for child in self.children:
            child.recursive_rebuild()

    def build(self):
        if self.is_built:
            return

        self.before_build()

        while not self.is_built:
            # If parent is suddenly not built, go back to parent before
            # continuing with building the child nodes (unwind).  This happens
            # when new instructions are dynamically inserted before current instruction.
            if self.parent and not self.parent.is_built:
                return

            self.is_built = True
            self.before_build_children()

            for child_idx, child in enumerate(self.children):
                self.before_build_child(child_idx, child)
                child.build()

                # Only build remaining children if child did not invalidate parent node
                if not self.is_built:
                    break

            # Only do final inner build once we stabilize
            if self.is_built:
                self.build_inner()

        self.after_build()

    def build_inner(self):
        pass

    def before_build(self):
        pass

    def before_build_children(self):
        pass

    def before_build_child(self, child_idx, child):
        pass

    def after_build(self):
        pass

    def to_ll_ast(self):
        raise NotImplementedError()

    def is_lvalue(self):
        if not self.parent:
            return False
        return self.parent.is_child_lvalue(self)

    def is_rvalue(self):
        if not self.parent:
            return False
        return self.parent.is_child_rvalue(self)

    def is_child_lvalue(self, child):
        return False

    def is_child_rvalue(self, child):
        return True

    def find_type_up(self, node_type, search_self=False):
        if search_self and isinstance(self, node_type):
            return self
        if not self.parent:
            return None
        if isinstance(self.parent, node_type):
            return self.parent
        return self.parent.find_type_up(node_type, search_self)

    def get_enclosing_module(self, search_self=False) -> "Module":
        from .module import Module
        return self.find_type_up(Module, search_self)

    def get_enclosing_func(self, search_self=False) -> "FuncDef":
        from .func_def import FuncDef
        return self.find_type_up(FuncDef, search_self)

    def get_enclosing_class(self, search_self=False) -> "ClassDef":
        from .class_def import ClassDef
        return self.find_type_up(ClassDef, search_self)

    def get_enclosing_scope(self, search_self=False) -> "VarScope":
        from .var_scope import VarScope
        return self.find_type_up(VarScope, search_self)

    def insert_instrs_before(self, node, instrs):
        self.parent.insert_instrs_before(self, instrs)
        self.set_rebuild()

    def insert_instrs_after(self, node, instrs):
        self.parent.insert_instrs_after(self, instrs)
        self.set_rebuild()

    def find_children_with_class(self, node_cls, out=None):
        if out is None:
            out = []

        for child in self.children:
            if isinstance(child, node_cls):
                out.append(child)
            child.find_children_with_class(node_cls, out)

        return out

    def get_ancestor_with_class(self, node_cls):
        if not self.parent:
            return None

        if isinstance(self.parent, node_cls):
            return self.parent

        return self.parent.get_ancestor_with_class(node_cls)
