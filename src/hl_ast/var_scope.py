from typing import List, Dict
from collections import OrderedDict, deque, defaultdict
from .node import Node
from src.exceptions import *
from .variable import Variable
import llvmlite.ir as ll


SymbolStack = Dict[str, Variable]


class VarScope(Node):
    def __init__(self, name, local_symbols = None, global_symbols = None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.global_symbols:SymbolStack = local_symbols or dict()
        self.local_symbols:SymbolStack = global_symbols or dict()
        self.func_tpls = OrderedDict()
        self.class_tpls = OrderedDict()
        self.funcs = OrderedDict()
        self.classes = OrderedDict()
        self.dead_refs = defaultdict(list)

    def before_build(self):
        self.func_tpls = OrderedDict()
        self.class_tpls = OrderedDict()
        self.local_symbols = dict()
        self.global_symbols = dict()
        self.dead_refs = defaultdict(list)

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


