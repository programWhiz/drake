from typing import List
from .type import Type


class Node:
    def __init__(self, parent=None, children=None, type:Type=None):
        self.parent:"Node" = parent
        self.children:List["Node"] = children or []
        for child in self.children:
            child.parent = self
        self.is_built = False
        self.type:Type = type

    def get_locals(self):
        return self.get_enclosing_scope().get_locals()

    def get_globals(self):
        return self.get_enclosing_scope().get_globals()

    def replace_child(self, node, repl_nodes):
        if not repl_nodes:
            return self.remove(node)

        index_of = self.children.index(node)
        self.children[index_of:index_of+1] = repl_nodes
        for node in repl_nodes:
            node.parent = self

    def remove(self, node):
        self.children.remove(node)

    def add(self, *nodes):
        if nodes:
            for node in nodes:
                node.parent = self
                self.children.append(node)

    def set_rebuild(self):
        self.is_built = False

    def build(self):
        if self.is_built:
            return

        self.before_build()

        while not self.is_built:
            self.is_built = True
            self.before_build_children()

            for child_idx, child in enumerate(self.children):
                self.before_build_child(child_idx, child)
                child.build()

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

    def find_type_up(self, node_type):
        if not self.parent:
            return None
        if isinstance(self.parent, node_type):
            return self.parent
        return self.parent.find_type_up(node_type)

    def get_enclosing_module(self) -> "Module":
        from .module import Module
        return self.find_type_up(Module)

    def get_enclosing_func(self) -> "FuncDef":
        from .func import FuncDef
        return self.find_type_up(FuncDef)

    def get_enclosing_class(self) -> "ClassDef":
        from .class_def import ClassDef
        return self.find_type_up(ClassDef)

    def get_enclosing_scope(self) -> "VarScope":
        from .var_scope import VarScope
        return self.find_type_up(VarScope)
