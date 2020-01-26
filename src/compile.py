import os
import re
import tempfile
from typing import List

from rply import ParsingError, Token, LexingError
from rply.token import SourcePosition

from src.cpp import ast_to_cpp
from src.lexer import lexer
from src.parser import parser, print_ast_debug


def compile_source(source:str):
    source = clean_source(source)

    try:
        tokens = list(lexer.lex(source))
    except LexingError as e:
        print_lexing_error(source, e)
        return

    tokens = indent_tokens(tokens)
    print_tokens(tokens)

    try:
        return parser.parse(iter(tokens))
    except ParsingError as e:
        print_parsing_error(source, e)


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
    prev_indent, indent = 0, 0
    indent_depth = 0
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

            if indent > prev_indent:
                indented_tokens.append(Token(
                    name="INDENT",
                    value=" ",
                    source_pos=token.source_pos))
                prev_indent = indent
                indent_depth += 1

            elif indent < prev_indent:
                indented_tokens.append(Token(
                    name="DEDENT",
                    value=" ",
                    source_pos=token.source_pos))
                prev_indent = indent
                indent_depth -= 1

            # else, indent is unchanged

        # Copy newlines not after other newlines
        elif token.name == "NEWLINE":
            indented_tokens.append(token)

        prev_token = token

    # At end of file, dedent to outermost level
    for i in range(indent_depth):
        indented_tokens.append(Token("DEDENT", "", source_pos=tokens[-1].source_pos))

    return indented_tokens


def print_tokens(tokens:List[Token]):
    print("\nTokens:")
    for line, token in enumerate(tokens, 1):
        print(line, token)
    print("\n")


if __name__ == '__main__':
    source = """
a = 3
b = 4
c = a + b
    """
    ast = compile_source(source)
    if ast is not None:
        print("AST Tree:")
        print_ast_debug(ast)

    cpp_code = ast_to_cpp(ast)
    print("\n\n=== CPP code ===\n", cpp_code)

    binary_path = tempfile.mktemp(suffix=".out", dir="/tmp")

    cpp_path = tempfile.mktemp(suffix=".cpp", dir="/tmp")
    with open(cpp_path, "wt") as fptr:
        fptr.write(cpp_code)

    if os.system(f'g++ "{cpp_path}" -o "{binary_path}"') == 0:
        print("Running binary", binary_path)
        os.system(binary_path)
        os.remove(binary_path)
    else:
        print("ERROR: Could not compile c++!")

    os.remove(cpp_path)




