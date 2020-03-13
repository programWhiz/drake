from collections import OrderedDict
from typing import List, Dict
from .type import Type
from .var_scope import VarScope
from .node import Node
import llvmlite.ir as ll
from .binding import BindInst
from ..llvm_ast import next_id


class ClassDef(VarScope):
    clone_attrs = [ 'fields' ]

    def __init__(self, fields=None, **kwargs):
        super().__init__(**kwargs)
        # Is this a class template, or concrete instance?
        self.build_as_instance = False
        self.fields:Dict[str, Type] = fields or OrderedDict()

    def after_build(self):
        # Don't declare variable to module scope if this is instantiation,
        # only declare during template discovery phase
        if not self.build_as_instance:
            self.get_enclosing_scope().put_scoped_var(self)


class ClassInst(Node):
    def __init__(self, class_def:ClassDef, bind_fields:Dict[str, Type], **kwargs):
        super().__init__(**kwargs)
        self.class_def = class_def.clone()
        self.bind_fields = bind_fields

    def before_build(self):
        # Bind all types to the internal class definition
        for name, dtype in self.bind_fields.items():
            self.class_def.fields[name] = dtype
