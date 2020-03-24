import sys
import antlr4

from src.error_listener import format_source_code_error
from src.exceptions import *


def ast_node_location(ast_node):
    if hasattr(ast_node, 'line'):
        loc = ast_node
    elif isinstance(ast_node, antlr4.TerminalNode):
        loc = ast_node.symbol
    else:
        loc = ast_node.start
    return { 'file': loc.source[1].fileName, 'line': loc.line, 'col': loc.column }


def ast_location_str(ast_node):
    loc = ast_node_location(ast_node)
    return f"In file \"{loc['file']}\" line {loc['line']} col {loc['col']}"


def ast_is_empty(ast_node):
    return ast_text_is(ast_node, ("<EOF>", "\n"))


def ast_text_is(ast_node, text):
    if not isinstance(text, (tuple, list)):
        text = (text,)
    return isinstance(ast_node, antlr4.TerminalNode) and ast_node.symbol.text in text


def raise_unknown_ast_node(ast_node):
    node_type = ast_node.__class__.__name__
    if isinstance(ast_node, antlr4.TerminalNode):
        ast_text = ast_node.symbol.text
    else:
        ast_text = ast_node.start.text

    loc_str = ast_location_str(ast_node)
    error = f"{loc_str}: Unhandled AST node type: {node_type}, `{ast_text}`"
    sys.stderr.write(f"Parse error {error}\n")

    print_source_code_error(ast_node)
    raise ParseException(error)


def print_source_code_error(ast_node):
    loc = ast_node_location(ast_node)
    source_code = open(loc['file'], 'rt').read()
    source_code_error = format_source_code_error(source_code, loc['line'], loc['col'])
    print(source_code_error, file=sys.stderr)


def term_text_equals(term_node, text):
    return isinstance(term_node, antlr4.TerminalNode) and term_node.symbol.text == text


def ast_node_text(ast_node):
    if isinstance(ast_node, antlr4.TerminalNode):
        return ast_node.symbol.text
    else:
        return ''.join(ast_node_text(child) for child in ast_node.children)
