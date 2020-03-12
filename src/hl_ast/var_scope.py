from typing import List, Dict
from collections import OrderedDict, deque, defaultdict
from .node import Node
from src.exceptions import *
from .variable import Variable
import llvmlite.ir as ll


SymbolStack = Dict[str, Variable]


class VarScope(Node):
    clone_attrs = [ 'name', 'global_symbols', 'local_symbols', 'func_tpls', 'funcs', 'classes', 'class_tpls', ]

    def __init__(self, name, local_symbols = None, global_symbols = None, func_tpls=None,
                 funcs=None, classes=None, class_tpls=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.global_symbols:SymbolStack = local_symbols or dict()
        self.local_symbols:SymbolStack = global_symbols or dict()
        self.funcs = funcs or OrderedDict()
        self.func_tpls = func_tpls or OrderedDict()
        self.classes = classes or OrderedDict()
        self.class_tpls = class_tpls or OrderedDict()
        self.dead_refs = defaultdict(list)

    def before_build(self):
        self.funcs = OrderedDict()
        self.func_tpls = OrderedDict()
        self.classes = OrderedDict()
        self.class_tpls = OrderedDict()
        self.local_symbols = dict()
        self.global_symbols = dict()
        self.dead_refs = defaultdict(list)

    def to_ll_ast(self):
        module = self.get_enclosing_module(search_self=True)

        for func_inst in self.funcs.values():
            module.ll_funcs.append(func_inst.to_ll_ast())

        return { "op": "pass" }

    def get_locals(self):
        return self.local_symbols

    def get_globals(self):
        return self.global_symbols

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
        func_inst = FuncInst(name=key, func_def=func_def, func_bind=func_bind, module=module)
        # Cache so there is only one instance of the function with this signature
        self.funcs[key] = func_inst
        return func_inst