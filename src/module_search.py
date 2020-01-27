import os
from pathlib import Path
from src.drake_ast import ImportStmnt


def fill_module_paths(ast, cur_module_name_list, cur_module_path, search_paths):
    imports = []
    for s in ast:
        if not isinstance(s, ImportStmnt):
            continue

        s.module.abs_path = get_module_path(s.module.name_dot_list, cur_module_path, search_paths)
        s.module.abs_name = get_full_module_name(s.module.name_dot_list, cur_module_name_list)

        imports.append(s)

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
