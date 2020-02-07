from src.code_graph_types import *


def calculate_types(block):
    for instr in block.instructions:
        pass


def find_var_up(block, name):
    if name in block.local_vars:
        return block.local_vars[name]
    elif name in block.global_vars:
        return block.global_vars[name]

    if block.parent:
        return find_var_up(block.parent, name)

    return None
