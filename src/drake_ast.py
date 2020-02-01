from typing import List

def print_indented(indent, text):
    print("  " * indent, text)


def print_ast_debug(node, indent=0):
    symbol = getattr(node, 'start', getattr(node, 'symbol', None))
    print_indented(indent, f"{node.__class__.__name__} : {symbol}")
    if hasattr(node, 'children') and node.children:
        for child in node.children:
            print_ast_debug(child, indent + 1)


def surf_ast(node, path):
    """
    :param node: an AST node to navigate.
    :param path: a slash separated list of node types, and can match regex.
        Ex: File_inputContext/StmtContext/Simple_stmtContext/Small_stmtContext/Import_stmtContext
        Ex: ./././Import_stmtContext/.
    :return: A list of AST nodes that match the query.  The classname of these nodes
        will match the final queried classname of the path.
    """

    if isinstance(node, (list, tuple)):
        nodes = node
    else:
        nodes = [ node ]

    for part in path.split('/'):
        nodes = [ child
                  for node in nodes if hasattr(node, 'children')
                  for child in node.children
                  if part == "." or child.__class__.__name__ == part ]
        if not nodes:
            return []

    return nodes


def surf_deep(node, exact_class):
    if not hasattr(node, 'children'):
        return None

    matches = [ child for child in node.children
        if child.__class__.__name__ == exact_class ]

    if matches:
        return matches

    matches = []
    for child in node.children:
        child_matches = surf_deep(child, exact_class)
        if child_matches:
            matches.extend(child_matches)

    return matches
