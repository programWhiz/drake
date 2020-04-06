import re
from abc import ABC
from collections import OrderedDict
from typing import List
from .type import Type
from .numeric import NumericType
from .var_scope import VarScope
from .variable import FuncParamVariable
from .node import Node
from ..id_utils import next_id, next_tmp_name
from src.exceptions import *


class ClassDef(VarScope):
    clone_attrs = [ 'fields', 'parent_cls' ]

    def __init__(self, fields:OrderedDict=None, parent_cls:List['ClassDef'] = None, **kwargs):
        super().__init__(**kwargs)
        assert fields is None or isinstance(fields, OrderedDict), "ClassDef `fields` must be ordered dict."
        self.fields = fields if fields else OrderedDict()
        self.instance_methods = {}
        self.default_ctor = None
        self.parent_cls = parent_cls or []

    def clone(self):
        clone = super().clone()
        for key, func in self.instance_methods.items():
            rel_path = self.get_path_to_node(func)
            clone_func = clone.get_node_at_path(rel_path)
            clone.instance_methods[key] = clone_func

        return clone

    def get_local_symbol(self, name):
        if name == 'me':
            return self
        return super().get_local_symbol(name)

    def get_inherited_fields(self):
        fields = OrderedDict()
        for cls in self.parent_cls:
            for key, value in cls.fields.items():
                if key in fields:
                    raise DuplicateFieldException(
                        f"Class {self.name} field {key} collides in multiple parent classes.")
                fields[key] = value

        for key, value in self.fields.items():
            if key in fields:
                raise DuplicateFieldException(
                    f"Class {self.name} field {key} is already defined in a parent class.")
            fields[key] = value
        return fields

    def select_fields_subset(self, bind_fields):
        all_fields = self.get_inherited_fields()
        return OrderedDict((key, bind_fields[key]) for key in all_fields.keys())

    def build_inner(self):
        # Create a local variable of class name, so we can refer to the class by name
        self.get_enclosing_scope().put_scoped_var(self)

        # Build the default ctor
        self.build_ctor()

    def put_scoped_var(self, var):
        from .func_def import FuncDef
        if isinstance(var, FuncDef):
            self.instance_methods[var.name] = var
        else:
            super().put_scoped_var(var)

    def build_ctor(self) -> "FuncDef":
        pass

    def get_dtor(self) -> "FuncDef":
        from .func_def import FuncDef
        dtor_name = self.get_fully_scoped_name() + '.dtor'
        return FuncDef(name=dtor_name, func_args=[])

    def get_inst_method(self, name):
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
    def __init__(self, name, class_def:ClassDef, bind_fields:List, parent_tpls:List['ClassTemplate'], **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.class_def = class_def
        self.class_id = hash(name)
        self.bind_fields = bind_fields
        self.parent_tpls = parent_tpls

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
        supers = [ tpl.cpp_name() for tpl in self.parent_tpls ]
        supers = ','.join(f'public {cls}' for cls in supers)
        if supers:
            supers = ' : ' + supers

        cls_name = self.cpp_name()

        b.h.emit(f"""\nclass {cls_name}{supers} {{\n
        public:\n""")

        with b.h.with_indent():
            for name in self.class_def.fields.keys():
                dtype = self.bind_fields[name].type.cpp_type()
                b.h.emit(f"{dtype} {name};\n")

        b.h.emit('\n};\n')


class ClassInst(Node):
    def __init__(self, class_def:ClassDef, **kwargs):
        super().__init__(**kwargs)
        self.class_def = class_def.clone()
        self.bind_fields = class_def.get_inherited_fields()
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
        return self.class_def.get_inst_method(func_name)

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
        return scope.get_class_template(self.class_def, self.bind_fields)

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


class CtorArgs(Node):
    def to_cpp(self, b, class_inst):
        raise NotImplementedError()

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
        class_inst, ctor_args = self.children[0], self.children[1]
        class_name = class_inst.cpp_type()
        tmp = next_tmp_name()
        class_no_ptr = class_name[:-1]

        # Invoke the constructor and assign to temp var on stack
        b.c.emit(f'{class_no_ptr} {tmp} = {class_no_ptr}(')
        # TODO: implement constructor call here
        # ctor_args.to_cpp(b, class_inst)
        b.c.emit(');\n')

        # Assign to the named variable using pointer
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
        class_inst, ctor_args = self.children
        self.type = class_inst

        stack_alloc = StackAllocClassInst(children=[ class_inst, ctor_args ])
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
        self.inst_method = None

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
        if self.field_idx >= 0:
            self.type = cls_inst.get_field_type(self.field_name)

        else:  # No such field, maybe method?
            self.inst_method = cls_inst.get_inst_method(self.field_name)
            if not self.inst_method:
                cls_name = cls_inst.name
                raise InvalidAttributeError(f"Class {cls_name} has no attribute {self.field_name}")

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

        b.c.emit(f'{varname}->')

        if self.inst_method:
            self.inst_method.to_cpp(b)
        else:
            b.c.emit(self.field_name)


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