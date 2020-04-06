from typing import List, Dict
from collections import OrderedDict, deque, defaultdict
from .node import Node
from src.exceptions import *
from .variable import Variable
import llvmlite.ir as ll
from pprint import pformat

SymbolStack = Dict[str, Variable]


class VarScope(Node):
    clone_attrs = [ 'name', 'global_symbols', 'local_symbols', 'funcs', 'classes' ]

    def __init__(self, name, local_symbols = None, global_symbols = None,
                 funcs=None, classes=None, class_tpls=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.global_symbols:SymbolStack = local_symbols or dict()
        self.local_symbols:SymbolStack = global_symbols or dict()
        self.funcs = funcs or OrderedDict()
        self.classes = classes or OrderedDict()
        self.class_tpls = class_tpls or OrderedDict()
        self.dead_refs = defaultdict(list)
        self.union_types = OrderedDict()

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls}({self.name}, {pformat(self.children)})'

    def before_build(self):
        self.funcs = OrderedDict()
        self.classes = OrderedDict()
        # self.class_tpls = OrderedDict()
        self.local_symbols = dict()
        self.global_symbols = dict()
        self.dead_refs = defaultdict(list)
        self.union_types = OrderedDict()

    def to_ll_ast(self):
        module = self.get_enclosing_module(search_self=True)

        for class_tpl in self.class_tpls.values():
            module.ll_classes.append(class_tpl.to_ll_ast())

        for func_inst in self.funcs.values():
            module.ll_funcs.append(func_inst.to_ll_ast())

        return { "op": "pass", "comment": self.__class__.__name__ }

    def to_cpp(self, b):
        for union in self.union_types.values():
            union.to_cpp_class(b)

        for class_tpl in self.class_tpls.values():
            class_tpl.to_cpp(b)

        for func_inst in self.funcs.values():
            func_inst.to_cpp(b)

    def get_local_symbol(self, name):
        return self.local_symbols.get(name)

    def get_global_symbol(self, name):
        return self.global_symbols.get(name)

    def put_scoped_var(self, var:Variable):
        if var.name in self.local_symbols:
            self.dead_refs[var.name].append(self.local_symbols[var.name])

        self.local_symbols[var.name] = var

    def get_scoped_var(self, name, local_only=False):
        if isinstance(name, Variable):
            name = name.name

        var = self.local_symbols.get(name)
        if var:
            return var

        if local_only:
            return None

        return self.global_symbols.get(name, None)

    def get_fully_scoped_name(self):
        names = deque([ self.name ])
        parent = self.parent
        while parent is not None:
            if isinstance(parent, VarScope):
                names.appendleft(parent.name)
            parent = parent.parent
        return '.'.join(names)

    def get_func_instance(self, func_def, func_bind):
        key = func_bind.get_type_name()
        key = f'{self.name}.{key}'
        if key in self.funcs:
            return self.funcs[key]

        from .func_def import FuncInst
        module = self.get_enclosing_module(search_self=True)
        func_inst = FuncInst(name=key, func_def=func_def, func_bind=func_bind, parent=module)
        # Cache so there is only one instance of the function with this signature
        self.funcs[key] = func_inst
        return func_inst

    def get_class_template(self, class_def, bind_fields):
        name = class_def.get_fully_scoped_name()
        # NOTE: fields is a superset of all fields in all superclasses
        fields = ','.join(field.type.shortname() for field in bind_fields.values())
        key = f"{name}<{fields}>" if fields else name

        existing = self.class_tpls.get(key)
        if existing:
            return existing

        parent_tpls = []
        for parent in class_def.parent_cls:
            parent_fields = parent.select_fields_subset(bind_fields)
            parent_tpl = self.get_class_template(parent, parent_fields)
            parent_tpls.append(parent_tpl)

        from .class_def import ClassTemplate
        tpl = ClassTemplate(name=key, class_def=class_def, bind_fields=bind_fields, parent_tpls=parent_tpls)
        self.class_tpls[key] = tpl
        return tpl

    def register_union_type(self, union):
        key = union.shortname()
        if key not in self.union_types:
            self.union_types[key] = union

    def insert_instrs_before(self, node, instrs):
        return insert_instrs_before_impl(self, node, instrs)

    def insert_instrs_after(self, node, instrs):
        return insert_instrs_after_impl(self, node, instrs)


def insert_instrs_before_impl(self, node, instrs):
    idx = self.children.index(node)
    if not isinstance(instrs, (list, tuple)):
        instrs = [ instrs ]
    self.children = self.children[:idx] + instrs + self.children[idx:]
    for child in self.children:
        child.parent = self
    self.set_rebuild()


def insert_instrs_after_impl(self, node, instrs):
    idx = self.children.index(node)
    if not isinstance(instrs, (list, tuple)):
        instrs = [ instrs ]
    self.children = self.children[:idx+1] + instrs + self.children[idx+1:]
    for child in self.children:
        child.parent = self
    self.set_rebuild()
