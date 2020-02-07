from src.code_graph_types import *


def resolve_code_graph(module):
    for instr in module.instructions:
        if isinstance(instr, Assign):
            resolve_assignment(instr)


def resolve_assignment(assign:Assign):
    # Assign can be a complex statement on the left
    left_symbol = resolve_symbol(assign.left_instr)
    right_symbol = resolve_symbol(assign.right_instr)


def resolve_symbol(block:Block, symbol:Instruction):
    if isinstance(symbol, BareName):
        if symbol.text in block.local_vars:
            return block.local_vars[symbol.text]
        elif symbol.text in block.global_vars:
            return block.global_vars[symbol.text]
    elif isinstance(symbol, Literal):
        return symbol
    elif isinstance(symbol)
