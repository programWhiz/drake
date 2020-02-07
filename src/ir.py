from .code_graph_types import *


def block_to_ir(block:Block):
    for instr in block.instructions:
        print(instr)
