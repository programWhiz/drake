import re
from abc import ABC
from collections import OrderedDict
from typing import List

from .type import Type, TypePtr
from .numeric import NumericType
from .var_scope import VarScope
from .variable import BareName, FuncParamVariable, Variable
from .node import Node
from ..llvm_ast import next_id, next_tmp_name
from src.exceptions import *


class ClassDef(VarScope):
    clone_attrs = [ 'fields' ]

    def __init__(self, fields:OrderedDict=None, **kwargs):
        super().__init__(**kwargs)
        assert fields is None or isinstance(fields, OrderedDict), "ClassDef `fields` must be ordered dict."
        self.fields = fields if fields else OrderedDict()
        self.instance_methods = {}
        self.default_ctor = None

    def build_inner(self):
        # Create a local variable of class name, so we can refer to the class by name
        self.get_enclosing_scope().put_scoped_var(self)

        # Build the default ctor
        self.build_ctor()

    def build_ctor(self) -> "FuncDef":
        if self.default_ctor:
            return

        from .func_def import FuncDef, FuncDefArg
        class_inst = ClassInst(class_def=self)
        ctor_name = self.get_fully_scoped_name() + '.ctor'
        args = [ FuncDefArg(name='me', index=0, dtype=class_inst) ]
        args.extend(
            FuncDefArg(
                name=field.name,
                index=index,
                dtype=field.type or field.default_value.type,
                default_val=field.default_value)
            for index, field in enumerate(self.fields.values(), 1))

        # Ctor just sets each field from the ctor args
        # Create instructions: me.x = x; me.y = y; ...
        ctor_body = []
        for field, ctor_arg in zip(self.fields.values(), args[1:]):
            get_field = GetAttr(children=[BareName('me'), GetAttrField(field.name)])
            arg_var = FuncParamVariable(func_arg=ctor_arg)
            setter = SetAttr(children=[ get_field, arg_var ])
            ctor_body.append(setter)

        self.default_ctor = FuncDef(name=ctor_name, func_args=args, children=ctor_body)

        self.instance_methods['ctor'] = self.default_ctor

        # Insert this into the parent module
        self.parent.insert_instrs_after(self, self.default_ctor)
        return self.default_ctor

    def get_dtor(self) -> "FuncDef":
        from .func_def import FuncDef
        dtor_name = self.get_fully_scoped_name() + '.dtor'
        return FuncDef(name=dtor_name, func_args=[])

    def get_instance_method(self, name):
        return self.instance_methods.get(name)


class ClassField:
    def __init__(self, name=None, type=None, default_value=None):
        self.name:str = name
        self.type:Type = type
        self.default_value = default_value

        def_type:Type = self.default_value and self.default_value.type

        if self.type and self.default_value:
            assert self.type.subsumes(def_type) or def_type.can_cast_to(self.type), \
                f"Default type {def_type} not compatible with field {self.name} of type {self.type}"

        elif not self.type and def_type:
            self.type = def_type


class ClassTemplate:
    def __init__(self, name, class_def:ClassDef, bind_fields:List, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.class_def = class_def
        self.class_id = hash(name)
        self.bind_fields = bind_fields

    def cpp_name(self):
        return re.sub(r'\W', '_', self.name)

    def to_ll_ast(self):
        return {
            "name": self.name,
            "type": "class",
            "id": self.class_id,
            "inst_vars": [
                { "name": name, "type": self.bind_fields[i].type.ll_type() }
                for i, name in enumerate(self.class_def.fields.keys())
            ]
        }

    def ll_ref(self):
        return {
            "type": "class",
            "id": self.class_id,
            "name": self.name,
        }

    def to_cpp(self, b):
        b.h.emit(f"""\nclass {self.cpp_name()} {{\n
        public:\n""")

        with b.h.with_indent():
            for i, name in enumerate(self.class_def.fields.keys()):
                dtype = self.bind_fields[i].type.cpp_type()
                b.h.emit(f"{dtype} {name};\n")

        b.h.emit('\n};\n')


class ClassInst(Node):
    def __init__(self, class_def:ClassDef, **kwargs):
        super().__init__(**kwargs)
        self.class_def = class_def.clone()
        self.bind_fields = OrderedDict(class_def.fields)
        self.ptr_id = next_id()
        self.cpp_var_name = f'ptr_{self.ptr_id}'

    def can_cast_to(self, other):
        return False

    @property
    def name(self):
        return self.class_def.name

    def shortname(self):
        return self.class_def.name

    def equivalent(self, other):
        return (
            isinstance(other, ClassInst) and
            other.class_def.name == self.class_def.name and
            set(self.bind_fields.keys()) == set(other.bind_fields.keys()) and
            all(f.type is None or f.type.equivalent(other.bind_fields[k].type)
                for k, f in self.bind_fields.items())
        )

    def get_inst_method(self, func_name):
        return self.class_def.instance_methods.get(func_name)

    def get_field_index(self, field_name):
        for i, key in enumerate(self.bind_fields.keys()):
            if key == field_name:
                return i
        return -1

    def get_field_type(self, field_name):
        return self.bind_fields[field_name].type

    def before_ll_ast(self):
        self.get_class_template()
        super().before_ll_ast()

    def before_cpp(self):
        self.get_class_template()
        super().before_cpp()

    def get_class_template(self):
        scope = self.get_enclosing_module()
        bind_fields = list(self.class_def.fields.values())
        return scope.get_class_template(self.class_def, bind_fields)

    def ll_type(self):
        return self.get_class_template().ll_ref()

    def __repr__(self):
        return "ClassInst"

    def to_ll_ast(self):
        class_ref = self.get_class_template().ll_ref()

        return {
            "id": self.ptr_id,
            "comment": repr(self),
            "type": {
                "type": "ptr",
                "class": class_ref
            }
        }

    def cpp_type(self):
        cpp_name = self.get_class_template().cpp_name()
        return cpp_name + '*'

    def to_cpp(self, b):
        b.c.emit(self.cpp_var_name)


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

    def to_cpp(self, b):
        class_inst = self.children[0]
        class_name = class_inst.cpp_type()
        tmp = next_tmp_name()
        class_no_ptr = class_name[:-1]
        b.c.emit(f'{class_no_ptr} {tmp};\n')
        b.c.emit(f'{class_name} {class_inst.cpp_var_name} = &{tmp};\n')


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
            "value": 0,
            "comment": repr(self) }

    def to_cpp(self, b):
        b.c.emit(self.children[0].cpp_var_name)


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

    def to_cpp(self, b):
        left, right = self.children
        left.to_cpp(b)
        b.c.emit(' = ')
        right.to_cpp(b)


class GetAttr(Node):
    clone_attrs = [ 'field_idx', 'field_name' ]

    def __init__(self, field_idx=None, field_name=None, **kwargs):
        super().__init__(**kwargs)
        self.field_idx = field_idx
        self.field_name = field_name

    def build_inner(self):
        var, attr_field = self.children
        if hasattr(var, 'var'):  # reference to variable
            var = var.var

        self.field_name = attr_field.field_name
        # If we are unable to resolve type (still in template or unresolved),
        # just use these as working assumptions
        self.field_idx = 0
        self.type = NumericType(precision=8, is_int=True)

        if isinstance(var, FuncParamVariable):
            # We don't know what type of param this is yet
            from .func_def import FuncDef
            func_def = var.get_ancestor_with_class(FuncDef)
            if var.type is None and not func_def.build_as_instance:
                return

        cls_inst = var.type
        assert isinstance(cls_inst, ClassInst), ('Got non-class var in GetAttr:' + repr(cls_inst))

        self.field_idx = cls_inst.get_field_index(self.field_name)
        if self.field_idx < 0:
            cls_name = cls_inst.name
            raise InvalidAttributeError(f"Class {cls_name} has no attribute {self.field_name}")

        self.type = cls_inst.get_field_type(self.field_name)

    def __repr__(self):
        child = repr(self.children[0])
        return f'GetAttr({child}, {self.field_name})'

    def to_cpp(self, b):
        child = self.children[0]

        if hasattr(child, 'var'):  # reference to variable
            varname = child.var.cpp_name()
        elif isinstance(child, FuncParamVariable):
            varname = child.func_arg.cpp_name()
        else:
            raise Exception(f"Unsupported child node type for GetAttr: {repr(child)}")

        b.c.emit(f'{varname}->{self.field_name}')

    def to_ll_ast(self):
        child = self.children[0]

        if hasattr(child, 'var'):  # reference to variable
            # This works if direct reference to class
            ref = child.var.ll_ref()
            # If pointer to class, dereference
            if child.var.is_class_ptr():
                ref = { 'op': 'load', 'ref': ref }

        elif isinstance(child, FuncParamVariable):
            # Func param is pointer to class, get the class instance from pointer
            ref = { 'op': 'gep', 'ref': child.to_ll_ast(), 'value': 0 }
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