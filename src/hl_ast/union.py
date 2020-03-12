from src.exceptions import *
from .type import Type
from .node import Node


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

        t1_types = set(t1.types) if isinstance(t1, UnionType) else { t1 }
        t2_types = set(t2.types) if isinstance(t2, UnionType) else { t2 }

        types = list(t1_types | t2_types)
        types.sort()

        if len(types) == 1:
            return next(iter(types))

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
            return other_tuple in self.types

    def to_tuple(self):
        return tuple(sorted(t.to_tuple() for t in self.types))

    def get_type_index(self, dtype:Type):
        type_index = next((i for i, xtype in enumerate(self.types) if dtype.equivalent(xtype)), -1)

        if type_index < 0:
            raise InvalidUnionTypeError(f"Tried to get invalid type {dtype} from Union.")

        if type_index > 255:
            raise TooManyAlternativesError(f"Variable {self.var.name} has more than 255 possible types.")

        return type_index

    def shortname(self):
        x = ','.join(t.shortname() for t in self.types)
        return f'[{x}]'

    def longname(self):
        x = ','.join(t.longname() for t in self.types)
        return f'[{x}]'


class GetUnionPointer(Node):
    clone_attrs = [ 'gep_index' ]

    def __init__(self, gep_index:int = None, **kwargs):
        super().__init__(**kwargs)
        self.gep_index = gep_index

    def build_inner(self):
        var = self.children[0]
        union = var.type
        self.gep_index = union.get_type_index(self.type)

    def to_ll_ast(self):
        return {
            "op": "gep",
            "ref": self.children[0].ll_ref(),
            "value": [ 0, self.gep_index ]
        }
