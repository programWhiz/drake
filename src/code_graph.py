from pathlib import Path
from src.module_search import fill_module_paths


def init_code_program(ast):
    program = Program()
    # TODO: associate each module's code to a module
    program.modules['__main__'] = Module(ast)


def compile_module_cached(program, abs_name, abs_path):
    from src.compile import compile_file, get_compile_target_file

    if abs_name in program.modules:
        return program.modules[abs_name]

    if '.' in abs_name:
        parent_name = abs_name.rsplit('.', 1)[0]
        parent_path = str(Path(abs_path).parent)
        compile_module_cached(program, parent_name, parent_path)

    abs_path = get_compile_target_file(abs_path)

    module = Module(
        ast=compile_file(abs_path),
        abs_name=abs_name,
        abs_path=abs_path)

    program.modules[abs_name] = module
    build_code_graph(program, module)

    return module


def build_code_graph(program, module):
    imports = fill_module_paths(module.ast, module.abs_name.split('.'), module.abs_path, program.search_paths)

    for im in imports:
        module.vars[im.module.name] = compile_module_cached(program=program,
            abs_name=im.module.abs_name, abs_path=im.module.abs_path)


class Program:
    def __init__(self):
        self.search_paths = []
        self.modules = {}


class Module:
    def __init__(self, ast=None, abs_path=None, abs_name=None):
        self.ast = ast
        self.abs_path = abs_path
        self.abs_name = abs_name
        self.vars = {}


class Func:
    def __init__(self):
        self.return_dtype = None
        self.args = None

class Var:
    def __init__(self):
        self.module = None
        self.func = None
        self.cls = None
        self.writes = []
        self.reads = []


class Literal:
    def __init__(self, dtype, value):
        self.dtype = dtype
        self.value = value
