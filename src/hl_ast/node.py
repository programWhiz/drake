from typing import List
from .type import Type


class Node:
    clone_attrs = [ 'type' ]

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
