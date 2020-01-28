from pathlib import Path
from src import drake_ast as dast
from src.module_search import find_module_imports


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
    imports = find_module_imports(module.ast, module.abs_name.split('.'), module.abs_path, program.search_paths)

    for im in imports:
        module.vars[im['local_name']] = compile_module_cached(
            program=program, abs_name=im['abs_name'], abs_path=im['abs_path'])

    return

    imports = find_symbol_imports(module.ast, module.abs_name.split('.'), module.abs_path, program.search_paths)
    for im in imports:
        imported_module = compile_module_cached(program, im['module_abs_name'], im['module_abs_path'])
        for symbol in im['import_symbols']:
            module.vars[symbol['local_name']] = imported_module[symbol['remote_name']]

    build_module_graph(program, module)


def build_module_graph(program, module):
    for stmnt in module.ast:
        if isinstance(stmnt, dast.FuncDef):
            build_func_graph(program, stmnt, module)
        elif isinstance(stmnt, dast.ClassDef):
            build_class_graph(program, stmnt, module)
        elif isinstance(stmnt, dast.InPlace):
            build_inplace_graph(program, stmnt, module)


def build_inplace_graph(program:"Program", stmnt:dast.InPlace, parent:"Block"):
    lhs_node = resolve_node(program, parent, stmnt.lhs)
    rhs_node = resolve_node(program, parent, stmnt.rhs)

    lhs_node.add_write_edge(rhs_node)
    rhs_node.add_read_edge(lhs_node)


def resolve_node(program:"Program", parent:"Block", stmnt:dast.Node):
    if not isinstance(stmnt, dast.VarNode):
        print(f"BUILD ERROR: Cannot resolve node of type {type(stmnt)}:\n", stmnt)
        raise BuildException("Cannot resolve node with type " + str(type(stmnt)))

    key, remain = stmnt.name_dot_list[0], stmnt.name_dot_list[1:]
    node = search_nodes_up(parent, key)
    if node is None:
        raise UndeclaredIdentifier(f"Use of undeclared identifier {key}")

    while remain:
        key, remain = remain[0], remain[1:]
        node = node.vars.get(key)
        if node is None:
            raise MissingAttribute(f"{node} has no attribute {key}")

    return node


def search_nodes_up(node:"Block", varname:str):
    if varname in node.vars:
        return node[varname]
    if node.parent:
        return search_nodes_up(node.parent, varname)
    return None

class Program:
    def __init__(self):
        self.search_paths = []
        self.modules = {}


class Block:
    def __init__(self, ast=None, ast_node=None, vars=None, blocks=None, parent=None):
        self.parent = parent
        self.ast = ast
        self.ast_node = ast_node
        self.vars = vars or {}
        self.blocks = blocks or []


class Module(Block):
    def __init__(self, ast=None, abs_path=None, abs_name=None, vars=None, blocks=None):
        super().__init__(ast=ast, ast_node=ast, vars=vars, blocks=blocks)
        self.abs_path = abs_path
        self.abs_name = abs_name


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


class BuildException(Exception):
    pass


class MissingAttribute(BuildException):
    pass

class UndeclaredIdentifier(BuildException):
    pass
