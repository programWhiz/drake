import re
from typing import List

from rply import ParsingError, Token, LexingError
from rply.token import SourcePosition

from src.lexer import lexer
from src.parser import parser


def compile(source:str):
    source = clean_source(source)

    try:
        tokens = list(lexer.lex(source))
    except LexingError as e:
        print_lexing_error(source, e)
        return

    tokens = indent_tokens(tokens)
    print_tokens(tokens)

    try:
        ast = parser.parse(iter(tokens))
        print('\nParse Tree:\n', ast)
    except ParsingError as e:
        print_parsing_error(source, e)


def clean_source(source:str) -> str:
    source = source.strip()
    # Make lines ending with backslash a continuation character
    source = re.sub(r'\\\s*\n', '', source)
    source += "\n"  # guarantee end with newline
    return source


def print_lexing_error(source:str, e:LexingError):
    print(f"Syntax error on line {e.source_pos.lineno}")
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

        elif token.name != "SPACE":
            indented_tokens.append(token)

        # If first token is space, or this space is after newline, treat as indent/dedent
        elif prev_token is None or prev_token.name == "NEWLINE":
            indent = token.source_pos.colno + len(token.value)
            if indent > prev_indent:
                token.name = "INDENT"
                prev_indent = indent
                indented_tokens.append(token)
                indent_depth += 1
            elif indent < prev_indent:
                token.name = "DEDENT"
                prev_indent = indent
                indented_tokens.append(token)
                indent_depth -= 1
            # else, indent is unchanged

        prev_token = token

    # At end of file, dedent to outermost level
    for i in range(indent_depth):
        indented_tokens.append(Token("DEDENT", "", source_pos=tokens[-1].source_pos))

    return indented_tokens


def print_tokens(tokens:List[Token]):
    print("\nTokens:")
    for line, token in enumerate(tokens, 1):
        print(line, token)


if __name__ == '__main__':
    source = """
    class Bar:
        def __init__(x):
            self.x = x
            
        def get_foo(self):
            return self.x
    """
    compile(source)


