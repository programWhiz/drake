import os
import re
import shutil
from typing import List
from rply import ParsingError, Token, LexingError
from rply.token import SourcePosition
from src.code_graph import Program, Module, build_code_graph
from src.cpp import ast_to_cpp
from src.lexer import lexer
from src.parser import parser, print_ast_debug


def compile_file(path:str):
    with open(path, 'rt') as fptr:
        source = fptr.read()
    return compile_source(source)


def get_compile_target_file(path:str) -> str:
    if os.path.isfile(path):
        return path

    if os.path.isdir(path):
        init_file = os.path.join(path, "__init__.dk")
        if not os.path.isfile(init_file):
            raise Exception(f"Missing __init__.dk file for directory {path}")

        return init_file


def compile_source(source:str):
    source = clean_source(source)

    try:
        tokens = list(lexer.lex(source))
    except LexingError as e:
        print_lexing_error(source, e)
        raise

    tokens = indent_tokens(tokens)
    print_tokens(tokens)

    try:
        return parser.parse(iter(tokens))
    except ParsingError as e:
        print_parsing_error(source, e)
        raise


def clean_source(source:str) -> str:
    source = source.strip()
    # Make lines ending with backslash a continuation character
    source = re.sub(r'\\\s*\n', '', source)
    source += "\n"  # guarantee end with newline
    return source


def print_lexing_error(source:str, e:LexingError):
    print(f"\nSyntax error on line {e.source_pos.lineno}")
    print_code_position_marker(source, e.source_pos)


def print_parsing_error(source:str, e:ParsingError):
    print(f"\nParser Error on line {e.source_pos.lineno}:")
    print_code_position_marker(source, e.source_pos)


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


def indent_tokens(tokens:List[Token]) -> List[Token]:
    # Figure out the indent / dedents
    prev_token = None
    indent_stack = []
    indent = 0, 0
    indented_tokens = []
    for token in tokens:
        # Treat semicolon like a newline
        if token.name == "SEMICOLON":
            indented_tokens.append(Token("NEWLINE", "\n", token.source_pos))

        # Just copy all tokens that are not space
        elif token.name not in ("SPACE", "NEWLINE"):
            indented_tokens.append(token)

        # If first token is space, or this space is after newline, treat as indent/dedent
        elif prev_token is None or prev_token.name == "NEWLINE":
            if token.name == "NEWLINE":
                indented_tokens.append(token)

            indent = token.source_pos.colno
            if token.name == "SPACE":
                indent += len(token.value)
            else:
                indent -= 1

            if indent > 0 and (not indent_stack or indent > indent_stack[-1]):
                indented_tokens.append(Token(
                    name="INDENT",
                    value=" ",
                    source_pos=token.source_pos))
                indent_stack.append(indent)

            while indent_stack and indent < indent_stack[-1]:
                indented_tokens.append(Token(
                    name="DEDENT",
                    value=" ",
                    source_pos=token.source_pos))
                indent_stack.pop()

            # else, indent is unchanged

        # Copy newlines not after other newlines
        elif token.name == "NEWLINE":
            indented_tokens.append(token)

        prev_token = token

    # At end of file, dedent to outermost level
    for _ in indent_stack:
        indented_tokens.append(Token("DEDENT", "", source_pos=tokens[-1].source_pos))

    return indented_tokens


def print_tokens(tokens:List[Token]):
    print("\nTokens:")
    for line, token in enumerate(tokens, 1):
        print(line, token)
    print("\n")


def compiler_test(test_name="factorial"):
    tests_dir = os.path.join(os.path.dirname(__file__), "..", "tests")
    source_dir = os.path.join(tests_dir, test_name)
    source_path = os.path.join(source_dir, 'main.dk')
    build_dir = os.path.join(source_dir, "build")
    binary_path = os.path.join(build_dir, f"{test_name}.out")
    cpp_path = os.path.join(build_dir, "main.cpp")

    ast = compile_file(source_path)
    print_ast_debug(ast)

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

    build_code_graph(program, cur_module)
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
