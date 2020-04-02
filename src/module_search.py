import os
from pathlib import Path
from src.ast_utils import *
from antlr4 import TerminalNode
from src.drake_ast import surf_ast
from src.grammar.DrakeParser import DrakeParser as DP


def find_module_imports(ast, cur_module_name_list, cur_module_path, search_paths):
    imports = []

    import_stmnts = surf_ast(ast, 'StmtContext/Simple_stmtContext/Small_stmtContext/Import_stmtContext/Import_nameContext/Dotted_as_namesContext/Dotted_as_nameContext')

    for node in import_stmnts:
        module_name_node = node.children[0]
        rel_name = ''.join(term.symbol.text for term in module_name_node.children)
        if len(node.children) == 1:   # no "as" statement after "import <rel_name>"
            local_name = rel_name
        else:  # using "import <rel_name> as <local_name>"
            local_name = node.children[-1].symbol.text

        name_dot_list = dot_split_module_name(rel_name)
        abs_path = get_module_path(name_dot_list, cur_module_path, search_paths)
        abs_name = get_full_module_name(name_dot_list, cur_module_name_list)

        imports.append({
            'ast_node': node, 'local_name': local_name, 'rel_name': rel_name,
            'name_dot_list': name_dot_list, 'abs_path': abs_path, 'abs_name': abs_name })

    return imports


def dot_split_module_name(module_name):
    parts = module_name.split('.')

    # If the module name ends with a dot, ignore last dot
    if parts[-1] == '':
        parts.pop()

    # Replace leading dots (now empty after split) with actual dots
    for i, part in enumerate(parts):
        if part != '':
            break  # done with leading dots
        parts[i] = '.'

    return parts


def import_from_module_name(node:DP.Import_fromContext):
    name, dot_list = "", []

    import_idx = next(i for i, child in enumerate(node.children) if isinstance(child, TerminalNode) and child.symbol.text == "import")
    # Take everything between "from" and "import"
    for child in node.children[1:import_idx]:
        if isinstance(child, TerminalNode):
            name += child.symbol.text
            dot_list.append(child.symbol.text)
        else:
            name += "".join(term.symbol.text for term in child.children)
            dot_list.extend([ term.symbol.text for term in child.children if term.symbol.text != "." ])

    return name, dot_list


def find_symbol_imports(ast, cur_module_name_list, cur_module_path, search_paths):
    imports = []

    import_stmnts = surf_ast(ast, 'StmtContext/Simple_stmtContext/Small_stmtContext/Import_stmtContext/Import_fromContext')

    for import_stmnt in import_stmnts:
        module_local_name, name_dot_list = import_from_module_name(import_stmnt)
        module_abs_path = get_module_path(name_dot_list, cur_module_path, search_paths)
        module_abs_name = get_full_module_name(name_dot_list, cur_module_name_list)
        import_symbols = []

        # For this "from", find "import <name>" and "import <name> as <alias>"
        for name_node in surf_ast(import_stmnt, 'Import_as_namesContext/Import_as_nameContext'):
            symbol_remote_name = ast_node_text(name_node.children[0])

            if len(name_node.children) == 3:  # <name> as <alias>
                symbol_local_name = name_node.children[2].symbol.text
            else:  # no "as" statement, import with same name
                symbol_local_name = symbol_remote_name

            import_symbols.append({
                'remote_name': symbol_remote_name,
                'local_name': symbol_local_name,
                'ast_node': name_node
            })

        imports.append({
            'module': {
                'abs_path': module_abs_path ,
                'abs_name': module_abs_name,
                'name_dot_list': name_dot_list,
                'local_name': module_local_name,
                'ast_node': import_stmnt,
            },
            'symbols': import_symbols
        })

    return imports


def get_full_module_name(module_name_list, cur_module_path):
    parent_dirs = 0
    for name in module_name_list:
        if name == '.':
            parent_dirs += 1
        else:
            break

    if parent_dirs == 0:
        final_path = module_name_list

    else:
        final_path = cur_module_path[:-parent_dirs] + module_name_list[parent_dirs:]

    return '.'.join(final_path)


def get_module_path(name_list, cur_module_path, search_paths):
    parent_dirs = 0
    for name in name_list:
        if name == '.':
            cur_module_path = str(Path(cur_module_path).parent)
            search_paths = [ cur_module_path ]
            parent_dirs += 1
        else:
            break

    name_list = name_list[parent_dirs:]

    matched_file = None

    for i, name in enumerate(name_list):
        next_dirs = []

        for dirname in search_paths:
            file_list = os.listdir(dirname)
            drake_file = f"{name}.dk"

            # If we have used all dotted module names in the list, we matched a file
            if drake_file in file_list and i >= len(name_list) - 1:
                matched_file = os.path.join(dirname, drake_file)
                break

            if name in file_list:
                next_dirs.append(os.path.join(dirname, name))
                continue  # matched a directory

        search_paths = next_dirs

    if matched_file:
        return matched_file

    elif len(search_paths) == 1:
        return search_paths[0]

    else:
        raise ModuleNotFoundError(f"Could not find module {'.'.join(name_list)} in {cur_module_path}")
