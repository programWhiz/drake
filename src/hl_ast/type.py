import llvmlite.ir as ll


class Type:
    def __init__(self, is_fixed:bool=False):
        self.is_fixed = is_fixed

    def ll_type(self):
        raise NotImplementedError()

    def __repr__(self):
        return self.shortname()

    def shortname(self) -> str:
        raise NotImplementedError()

    def longname(self) -> str:
        raise NotImplementedError()

    def is_primitive(self):
        return False

    def equivalent(self, other):
        return other == self

    def subsumes(self, other):
        return other is None or self.equivalent(other)

    def to_tuple(self):
        return tuple()

    def can_cast_to(self, other):
        return False

    def get_cast_to_func(self, other):
        return None


class VoidType(Type):
    def ll_type(self):
        return ll.VoidType()

    def is_primitive(self):
        return True

    def equivalent(self, other):
        return isinstance(other, VoidType)

    def to_tuple(self):
        return (VoidType,)

    def shortname(self) -> str:
        return 'v'

    def longname(self) -> str:
        return 'void'


class TypePtr(Type):
    def __init__(self, pointee:Type, **kwargs):
        super().__init__(**kwargs)
        self.pointee = pointee

    def shortname(self) -> str:
        return f'p<{self.pointee.shortname()}>'

    def longname(self) -> str:
        return f'ptr<{self.pointee.longname()}>'

    def equivalent(self, other):
        return isinstance(other, TypePtr) and \
               self.pointee.equivalent(other.pointee)

    def ll_type(self):
        return { 'type': 'ptr', 'pointee': self.pointee.ll_type() }
