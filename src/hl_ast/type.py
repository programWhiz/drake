class Type:
    def __init__(self):
        pass

    def ll_type(self):
        raise NotImplementedError()

    def is_primitive(self):
        return False

    def equivalent(self, other):
        return other == self

    def subsumes(self, other):
        return self.equivalent(other)

    def to_tuple(self):
        return tuple()

    def can_cast_to(self, other):
        return False

    def get_cast_to_func(self, other):
        return None


