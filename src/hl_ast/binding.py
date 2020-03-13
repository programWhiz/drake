
class BindInst:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.is_built = False

    def find_type_up(self, dtype, search_self):
        if self.parent and dtype is type(self.parent):
            return self.parent
        else:
            return None

    def build(self):
        if not self.is_built:
            self.build_inner()
            self.is_built = True

    def build_inner(self):
        raise NotImplementedError()

    def to_ll_ast(self):
        raise NotImplementedError()
