import llvmlite.ir as ll
from src.llvm_ast import next_id
from .var_scope import VarScope


class Module(VarScope):
    def __init__(self, is_main:bool=False, **kwargs):
        super().__init__(**kwargs)
        self.is_main = is_main

    def to_ll_ast(self):
        self.build()

        instrs = [ child.to_ll_ast() for child in self.children ]
        instrs.append({ 'op': 'ret_void' })

        # wrap instructions into init func, returning void
        init_func_inner = {
            "name": f"module.{self.name}.$init_inner",
            "args": [],
            "ret": { "type": ll.VoidType() },
            "id": next_id(),
            "instrs": instrs
        }
        # Call inner func from an "if module init" check initialize function
        init_func = module_init_func_ll_ast(self.name, init_func_inner['id'])
        funcs = [ init_func_inner, init_func ]

        # Call init from main method if this module is main
        if self.is_main:
            funcs.append(main_method_ll_ast(init_func['id']))

        return { "name": self.name, "instrs": instrs, "funcs": funcs, "classes": [] }


def main_method_ll_ast(entry_func_id):
    argc = ll.IntType(32)
    argv = ll.PointerType(ll.PointerType(ll.IntType(8)))
    return {
        'name': 'main',
        'ret': { 'type': ll.IntType(32) },
        'args': [ { 'type': argc }, { 'type': argv } ],
        'instrs': [
            {
                'op': 'call',
                'func': { "id": entry_func_id },
                'args': []
            },
            { 'op': 'ret', 'value': { 'op': 'const_val', 'value': ll.Constant(ll.IntType(32), 0) } }
        ]
    }


def module_init_func_ll_ast(module_name, entry_func_id):
    i1 = ll.IntType(8)
    zero, one = ll.Constant(i1, 0), ll.Constant(i1, 1)

    # declare global is_module_init = False
    global_instr = {
        'op': 'global_var',
        'align': 1,
        'name': '$module.is_init',
        'type': i1,
        'value': zero,
        'id': next_id()
    }

    ref = { 'id': global_instr['id'] }

    # if is_module_init:
    #   return
    # else:
    #   is_module_init = true
    if_cond = {
        'op': 'if',
        'cond': {
            'op': 'u==',
            'left': { 'op': 'load', 'ref': ref },
            'right': { 'op': 'const_val', 'type': i1, 'value': zero }
        },
        'true': [
            { 'op': 'store', 'ref': ref,
              'value': { 'op': 'const_val', 'type': i1, 'value': one } },
            { 'op': 'call', 'func': { 'id': entry_func_id }, 'args': [] },
            { 'op': 'ret_void' }
        ],
        'false': [ { 'op': 'ret_void' } ]
    }

    return {
        "name": f"module.{module_name}.$init",
        "args": [],
        "ret": { "type": ll.VoidType() },
        "id": next_id(),
        "instrs": [global_instr, if_cond],
    }
