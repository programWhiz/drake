import os
from pathlib import Path

import networkx as nx
from collections import defaultdict

import jinja2
from src.drake_ast import *


def ast_to_cpp(ast, cur_module_name_list, cur_module_path, search_paths) -> str:
    fill_module_paths(ast, cur_module_name_list, cur_module_path, search_paths)
    # detect_cirular_imports(modules_asts, module_paths)
    build_code_graph(ast)

    code = Code()
    add_standard_includes(code)

    for module_name, ast in modules_asts:
        render_module(code, module_name, ast)

    return code.render()


class Code:
    def __init__(self):
        self.includes = []
        self.predef_classes = []
        self.predef_funcs = []

    def render(self):
        templates_path = os.path.join(os.path.dirname(__file__), 'templates')
        loader = jinja2.FileSystemLoader(templates_path)
        env = jinja2.Environment(loader=loader, autoescape=False)
        tpl = env.get_template("main.cpp")
        return tpl.render(self.get_template_vars())

    def get_template_vars(self) -> dict:
        return self.__dict__


def add_standard_includes(code:Code):
   code.includes.extend([
       "<vector>",
       "<string>",
       "<iostream>",
       "<fstream>",
       "<map>",
       "<set>",
       "<unordered_map>",
   ])


def detect_cirular_imports(modules_asts):
    G = nx.DiGraph()
    indices_to_names = {}
    names_to_indices = {}

    # First map all module names to our graph
    for module_name, ast in modules_asts:
        if module_name not in names_to_indices:
            idx = len(names_to_indices) + 1
            names_to_indices[module_name] = idx
            indices_to_names[idx] = module_name
            G.add_node(idx)

    for module_name, ast in modules_asts:
        for stmnt in ast:
            if isinstance(stmnt, ImportStmnt):
                get_full_module_name()

    try:
        cycle_edges = nx.find_cycle(G)
        import_list = ", ".join(indices_to_names[i] for i in cycle_edges)
        import_list += ", " + indices_to_names[cycle_edges[-1][1]]
        raise Exception(f"Found cyclic imports: {import_list}")
    except nx.NetworkXNoCycle:
        pass


def render_module(code, module_name, ast):
    for stmnt in ast:
        # Skip statements that are pass at module level
        if isinstance(stmnt, PassStmnt):
            continue

        # predefine classes
        if isinstance(stmnt, ClassDef):
            code.predef_classes.append(stmnt.name)
            render_class(code, stmnt)

        if isinstance(stmnt, FuncDef):
            code.predef_funcs.append(stmnt.name)
            render_function(code, stmnt)


def get_func_signature(code, stmnt:FuncDef):
    pass


def render_function(code, stmnt:FuncDef):
    pass


def render_class(code, stmnt):
    pass

