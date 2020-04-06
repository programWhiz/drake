
class Program():
    def __init__(self):
        self.build_dir = ""
        self.search_paths = []
        self.modules = { }


class Module():
    def __init__(self, abs_path=None, abs_name=None, name=None):
        self.abs_path = abs_path
        self.abs_name = abs_name
        self.name = name or self.abs_name.split('.')[-1]
