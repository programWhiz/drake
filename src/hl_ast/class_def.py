from abc import ABC
from collections import OrderedDict
from typing import List
from .type import Type
from .var_scope import VarScope, Variable
from .node import Node
from ..llvm_ast import next_id
from src.exceptions import *


class ClassDef(VarScope):
    clone_attrs = [ 'fields' ]

    def __init__(self, fields:OrderedDict=None, **kwargs):
        super().__init__(**kwargs)
        assert fields is None or isinstance(fields, OrderedDict), "ClassDef `fields` must be ordered dict."
        self.fields = fields if fields else OrderedDict()

    def build_inner(self):
        # Create a local variable of class name, so we can refer to the class by name
        self.get_enclosing_scope().put_scoped_var(self)

    def get_ctor(self) -> "FuncDef":
        from .func_def import FuncDef
        ctor_name = self.get_fully_scoped_name() + '.ctor'
        return FuncDef(name=ctor_name, func_args=[])

    def get_dtor(self) -> "FuncDef":
        from .func_def import FuncDef
        dtor_name = self.get_fully_scoped_name() + '.dtor'
        return FuncDef(name=dtor_name, func_args=[])


class ClassTemplate:
    def __init__(self, name, class_def:ClassDef, bind_fields:List, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.class_def = class_def
        self.class_id = next_id()
        self.bind_fields = bind_fields

    def to_ll_ast(self):
        return {
            "name": self.name,
            "type": "class",
            "id": self.class_id,
            "inst_vars": [
                { "name": name, "type": self.bind_fields[i].ll_type() }
                for i, name in enumerate(self.class_def.fields.keys())
            ]
        }

    def ll_ref(self):
        return {
            "type": "class",
            "id": self.class_id,
            "name": self.name,
        }


class ClassInst(Node):
    def __init__(self, class_def:ClassDef, **kwargs):
        super().__init__(**kwargs)
        self.class_def = class_def.clone()
        self.bind_fields = OrderedDict(class_def.fields)
        self.ptr_id = next_id()

    @property
    def name(self):
        return self.class_def.name

    def equivalent(self, other):
        return isinstance(other, ClassInst) and \
            other.class_def == self.class_def and \
            all(f is None or f.equivalent(other.bind_fields[k]) for k, f in self.bind_fields.items())

    def get_field_index(self, field_name):
        for i, key in enumerate(self.bind_fields.keys()):
            if key == field_name:
                return i
        return -1

    def get_field_type(self, field_name):
        return self.bind_fields[field_name]

    def before_ll_ast(self):
        self.class_tpl = self.get_class_template()
        super().before_ll_ast()

    def get_class_template(self):
        scope = self.get_enclosing_scope()
        bind_fields = list(self.class_def.fields.values())
        return scope.get_class_template(self.class_def, bind_fields)

    def ll_type(self):
        return self.class_tpl.ll_ref()

    def __repr__(self):
        return "ClassInst"

    def to_ll_ast(self):
        class_ref = self.class_tpl.ll_ref()

        return {
            "id": self.ptr_id,
            "comment": repr(self),
            "type": {
                "type": "ptr",
                "class": class_ref
            }
        }


class StackAllocClassInst(Node):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f'StackAllocClassInst({repr(self.children[0])})'

    def build_inner(self):
        self.type = self.children[0]

    def to_ll_ast(self):
        ll_ref = self.children[0].to_ll_ast()
        return {
            "op": "alloca",
            "comment": repr(self),
            "ref": ll_ref,
            "type": ll_ref['type'] }


class DerefClassPtr(Node):
    def __repr__(self):
        return f'DerefClassPtr({repr(self.children[0])})'

    def build_inner(self):
        self.type = self.children[0]

    def to_ll_ast(self):
        ll_ref = self.children[0].to_ll_ast()
        return {
            "op": "gep",
            "ref": ll_ref,
            "value": 0, "comment": repr(self) }


class AllocClassInst(Node):
    def build_inner(self):
        self.type = self.children[0]
        class_inst = self.children[0]
        stack_alloc = StackAllocClassInst(children=[ class_inst ])
        ptr_deref = DerefClassPtr(children=[ class_inst ])
        self.insert_instrs_before(self, stack_alloc)
        self.parent.replace_child(self, [ ptr_deref ])
        self.is_built = True  # don't build again


class SetAttr(Node):
    def __repr__(self):
        left, right = self.children
        return f'SetAttr({repr(left)}, {repr(right)})'

    def to_ll_ast(self):
        left, right = self.children
        return {
            'op': 'store',
            'comment': repr(self),
            'ref': left.to_ll_ast(),
            'value': right.to_ll_ast()
        }

    def is_child_lvalue(self, child):
        return child == self.children[0]

    def is_child_rvalue(self, child):
        return child == self.children[1]


class GetAttr(Node):
    def build_inner(self):
        var, attr_field = self.children
        if hasattr(var, 'var'):  # reference to variable
            var = var.var

        cls_inst = var.type
        self.field_name = attr_field.field_name
        self.field_idx = cls_inst.get_field_index(self.field_name)
        if self.field_idx < 0:
            cls_name = cls_inst.name
            raise InvalidAttributeError(f"Class {cls_name} has no attribute {self.field_name}")

        self.type = cls_inst.get_field_type(self.field_name)

    def __repr__(self):
        child = repr(self.children[0])
        return f'GetAttr({child}, {self.field_name})'

    def to_ll_ast(self):
        child = self.children[0]
        if hasattr(child, 'var'):  # reference to variable
            # This works if direct reference to class
            ref = child.var.ll_ref()
            # If pointer to class, dereference
            if child.var.is_class_ptr():
                ref = { 'op': 'load', 'ref': ref }

        else:
            raise Exception('Expected child with `var` attribute: ' + repr(child))

        ast = {
            "op": "gep",
            "comment": repr(self),
            "ref": ref,
            "value": [ 0, self.field_idx ]
        }

        if self.is_rvalue():
            ast = { 'op': 'load', 'ref': ast }

        return ast


class GetAttrField(Node):
    clone_attrs = [ 'field_name' ]

    def __init__(self, field_name, **kwargs):
        super().__init__(**kwargs)
        self.field_name = field_name
