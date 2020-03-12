import llvmlite.ir as ll


class Type:
    def __init__(self):
        pass

    def ll_type(self):
        raise NotImplementedError()

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
