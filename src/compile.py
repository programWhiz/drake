import os
import re
import shutil
from src.code_graph import Program, Module, build_code_graph
from src.cpp import ast_to_cpp
from src.error_listener import DrakeErrorListener
from src.grammar.DrakeLexer import DrakeLexer
from antlr4 import InputStream, FileStream
from src.drake_ast import print_ast_debug
from src.grammar.DrakeParser import DrakeParser, CommonTokenStream


def compile_file(path:str):
    print("Parsing file", path)
    print_lexer_debug(path, FileStream(path))
    return compile_stream(path, FileStream(path))


def compile_string(source:str):
    return compile_stream("__main__", InputStream(source))


def get_compile_target_file(path:str) -> str:
    if os.path.isfile(path):
        return path

    if os.path.isdir(path):
        init_file = os.path.join(path, "__init__.dk")
        if not os.path.isfile(init_file):
            raise Exception(f"Missing __init__.dk file for directory {path}")

        return init_file


def print_lexer_debug(file_path, input_stream):
    print("Lexer symbols for", file_path)
    lexer = DrakeLexer(input_stream)
    type_names = { getattr(lexer, name, -1): name for name in lexer.symbolicNames }
    for tok in lexer.getAllTokens():
        text = tok.text
        name = type_names.get(tok.type, '<INVALID>')
        if text == "\n":
            text = "\\n"
        elif text == "\t" or re.match(r'^\s+$', text):
            text, name = "\\t", "TAB"

        print(tok.line, tok.start, text, name)


def compile_stream(file_path, input_stream):
    lexer = DrakeLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = DrakeParser(tokens)
    parser.addErrorListener(DrakeErrorListener(file_path))
    ast = parser.file_input()
    print_ast_debug(ast)
    return ast


def compiler_test(test_name="factorial"):
    tests_dir = os.path.join(os.path.dirname(__file__), "..", "tests")
    source_dir = os.path.join(tests_dir, test_name)
    source_path = os.path.join(source_dir, 'main.dk')
    build_dir = os.path.join(source_dir, "build")
    binary_path = os.path.join(build_dir, f"{test_name}.out")
    cpp_path = os.path.join(build_dir, "main.cpp")

    ast = compile_file(source_path)

    search_paths = [ source_dir ]
    cur_module_name_list = [ "tests", test_name, "main" ]
    cur_module_name = ".".join(cur_module_name_list)

    cur_module = Module()
    cur_module.abs_path = os.path.abspath(source_dir)
    cur_module.abs_name = cur_module_name
    cur_module.ast = ast
    cur_module.ast_node = ast

    program = Program()
    program.search_paths = search_paths
    program.build_dir = os.path.join(source_dir, "build")
    os.makedirs(program.build_dir, exist_ok=True)
    program.modules["__main__"] = cur_module
    program.modules[cur_module.abs_name] = cur_module

    cur_module.program = program

    graph = build_code_graph(cur_module)
    return

    cpp_code = ast_to_cpp(ast, cur_module_name_list, source_path)
    print("\n\n=== CPP code ===\n", cpp_code)

    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)
    os.mkdir(build_dir)

    with open(cpp_path, "wt") as fptr:
        fptr.write(cpp_code)

    assert os.system(f'g++ "{cpp_path}" -o "{binary_path}"') == 0

    print("Running binary", binary_path)
    assert os.system(binary_path) == 0


if __name__ == '__main__':
    compiler_test("simple_assign")
