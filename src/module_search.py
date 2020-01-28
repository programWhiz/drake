import os
from pathlib import Path
# from src.drake_ast import ImportStmnt
from typing import Dict, List

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

        name_dot_list = rel_name.split('.')
        abs_path = get_module_path(name_dot_list, cur_module_path, search_paths)
        abs_name = get_full_module_name(name_dot_list, cur_module_name_list)

        imports.append({
            'local_name': local_name, 'rel_name': rel_name,
            'name_dot_list': name_dot_list, 'abs_path': abs_path, 'abs_name': abs_name })

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

            # At most one symbol left
            if drake_file in file_list and i >= len(name_list) - 2:
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
        raise ModuleNotFoundError(f"Could not find module {'.'.join(name_list)}")
