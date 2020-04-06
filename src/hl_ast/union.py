import re
from collections import OrderedDict
from src.exceptions import *
from .type import Type
from .node import Node
from .numeric import NumericType, BoolType
from src.id_utils import next_id
import llvmlite.ir as ll


class UnionType(Type):
    def __init__(self, types, **kwargs):
        super().__init__(**kwargs)
        self.types = types

    @classmethod
    def make_union(cls, t1, t2):
        # If either type is None, union is the defined type
        if t1 is None or t2 is None:
            return t1 or t2

        if t1.equivalent(t2):
            return t1

        def types_dict(T):
            if isinstance(T, UnionType):
                return { t.shortname(): t for t in T.types }
            return { T.shortname() : T }

        types = types_dict(t1)
        types.update(types_dict(t2))
        types = list(sorted(types.items()))
        types = [ t[1] for t in types ]   # drop type names

        if len(types) == 1:
            return types[0]

        return UnionType(types=types)

    def equivalent(self, other):
        if not isinstance(other, UnionType):
            return False
        return other.to_tuple() == self.to_tuple()

    def subsumes(self, other):
        self_types = set(self.to_tuple())
        other_tuple = other.to_tuple()

        if isinstance(other, UnionType):
            other_types = set(other_tuple)
            return len(self_types.intersection(other_types)) == len(other_types)

        else:
            return other_tuple in self_types

    def to_tuple(self):
        return tuple(sorted(t.to_tuple() for t in self.types))

    def get_type_index(self, dtype:Type):
        type_index = next((i for i, xtype in enumerate(self.types) if dtype.equivalent(xtype)), -1)

        if type_index < 0:
            raise InvalidUnionTypeError(f"Tried to get invalid type {dtype} from Union.")

        if type_index > 255:
            raise InvalidUnionTypeError(f"Too many types! Implicit union only supports up to 255 types.")

        return type_index

    def shortname(self):
        x = ','.join(t.shortname() for t in self.types)
        return f'U<{x}>'

    def longname(self):
        x = ','.join(t.longname() for t in self.types)
        return f'Union<{x}>'

    def cpp_name(self):
        return re.sub(r'\W', '_', self.shortname())

    def cpp_type(self):
        return self.cpp_name()

    def to_cpp_class(self, b):
        name = self.cpp_name()
        union_name = f'Union_{name}'

        b.h.emit(f'\nunion {union_name} {{\n')
        with b.h.with_indent():
            for i, type in enumerate(self.types):
                b.h.emit(f'{type.cpp_type()} x{i};\n')
        b.h.emit('};\n')

        b.h.emit(f'\nclass {name} {{\n')
        with b.h.with_indent():
            b.h.emit('public:\n')
            b.h.emit(f'int type_idx;\n')
            b.h.emit(f'{union_name} types;\n')
        b.h.emit('};\n')

    def generate_switch(self, instr_callback, node):
        from .if_else import Switch, SwitchCase
        cases = []

        for type_idx, type in enumerate(self.types):
            # Get an altered instruction for the new type
            case_cond = UnionTypeCheck(type_idx=type_idx, children=[ node ])

            # Clone the node in question, but replace type
            node_with_cast = CastUnionValue(children=[node.clone()], type=type, type_idx=type_idx)

            # Now get an instruction that wraps the clone
            case_body = instr_callback(node_with_cast)

            cases.append(SwitchCase(children=[ case_cond, case_body ]))

        return Switch(children=cases)


class CastUnionValue(Node):
    clone_attrs = [ 'type_idx' ]

    def __init__(self, type_idx:int = None, **kwargs):
        super().__init__(**kwargs)
        self.type_idx = type_idx

    def to_cpp(self, b):
        b.c.emit('(')
        self.children[0].to_cpp(b)
        b.c.emit(f').types.x{self.type_idx}')


class UnionInst(Node):
    type_idx_bits = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ptr_id = next_id()

    def get_class_template(self):
        scope = self.get_enclosing_module()

        i8 = NumericType(is_int=True, is_fixed=True, precision=self.type_idx_bits)
        i64 = NumericType(is_int=True, is_fixed=True, precision=64)

        from .class_def import ClassDef, ClassField

        class_def = ClassDef(fields=OrderedDict({
            'type_id': ClassField(name='type_id', type=i8),
            'value': ClassField(name='value', type=i64)
        }))

        bind_fields = [ i8, i64 ]

        return scope.get_class_template(class_def, bind_fields)

    def __repr__(self):
        return self.type.shortname()

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


class StackAllocUnion(Node):
    def __repr__(self):
        return 'StackAllocUnion'

    def build_inner(self):
        ll_ref = self.children[0].to_ll_ast()

        return {
            "op": "alloca",
            "comment": repr(self),
            "ref": ll_ref,
            "type": ll_ref['type']
        }


class UnionTypeCheck(Node):
    clone_attrs =  [ 'type_idx' ]

    def __init__(self, type_idx, **kwargs):
        super().__init__(**kwargs)
        self.type_idx = type_idx
        self.type = BoolType()

    def to_cpp(self, b):
        b.c.emit('(')
        self.children[0].to_cpp(b)
        b.c.emit(f').type_idx == {self.type_idx}')

