import os
import re
import shutil
from typing import List
from rply import ParsingError, Token, LexingError
from rply.token import SourcePosition
from src.code_graph import Program, Module, build_code_graph
from src.cpp import ast_to_cpp
from src.grammar.DrakeLexer import DrakeLexer
from antlr4 import InputStream, FileStream
from src.drake_ast import print_ast_debug

from src.grammar.DrakeParser import DrakeParser, CommonTokenStream


def compile_file(path:str):
    print("Parsing file", path)
    return compile_stream(FileStream(path))


def compile_string(source:str):
    return compile_stream(InputStream(source))


def get_compile_target_file(path:str) -> str:
    if os.path.isfile(path):
        return path

    if os.path.isdir(path):
        init_file = os.path.join(path, "__init__.dk")
        if not os.path.isfile(init_file):
            raise Exception(f"Missing __init__.dk file for directory {path}")

        return init_file


def compile_stream(input_stream):
    lexer = DrakeLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = DrakeParser(tokens)
    ast = parser.file_input()
    print_ast_debug(ast)
    return ast


def print_code_position_marker(source:str, pos:SourcePosition, scope:int=4):
    lines = source.split('\n')
    start_line = max(pos.lineno - scope, 0)
    end_line = min(pos.lineno + scope + 1, len(lines))
    arrow_marker, empty_marker = ">>> ", "    "
    for i in range(start_line, end_line):
        line = lines[i]
        line_no_prefix = f"{i}.\t"

        if i == pos.lineno - 1:
            print(f"{arrow_marker}{line_no_prefix}{line}")
            num_spaces = len(arrow_marker) + len(line_no_prefix) + pos.colno
            spaces = " " * num_spaces
            print(f"{spaces}^")
        else:
            print(f"{empty_marker}{line_no_prefix}{line}")


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

    program = Program()
    program.search_paths = search_paths
    program.modules["__main__"] = cur_module
    program.modules[cur_module.abs_name] = cur_module

    cur_module.program = program

    build_code_graph(cur_module)
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
    compiler_test("import_test")
