import llvmlite.ir as ll
from src.exceptions import *


def compile_module_ir(module):
    ll_mod = ll.Module(name=module["name"])
    for key, func in module.get("funcs", {}).items():
        compile_func_ir(ll_mod, func)
    return ll_mod


def compile_module_init_func(module):
    """Constructs the module init function"""
    fntype = ll.FunctionType(ll.VoidType(), [])

    init_func = ll.Function(module, fntype, name=f'$init_module_{module["abs_name"]}')
    init_func_build = ll.IRBuilder()
    init_func_build.position_at_end(init_func.append_basic_block())

    for instr in module.get("instrs", []):
        instr.build_llvm_ir(init_func_build)

    init_func_build.ret_void()
    return module


def compile_func_ir(module, func):
    arg_types = [ arg["type"] for arg in func["args"] ]
    fntype = ll.FunctionType(func["ret"]["type"], arg_types)
    ll_func = ll.Function(module, fntype, name=func["name"])
    block = ll_func.append_basic_block()
    bb = ll.IRBuilder()
    bb.position_at_end(block)

    scope = { "module": module, "func": func, "ll_func": ll_func, "ptrs": {} }
    for instr in func["instrs"]:
        compile_instruction_ir(bb, instr, scope)


llvm_binary_ops = { 'add', 'fadd', 'sub', 'fsub', 'mul', 'fmul', 'sdiv', 'udiv', 'fdiv', 'and_', 'or_', 'xor' }

llvm_zero_ops = { 'ret_void' }

llvm_one_ops = { 'ret', }


def compile_instruction_ir(bb, instr, scope):
    op = instr['op']

    if op in llvm_binary_ops:
        left = compile_instruction_ir(bb, instr["left"], scope)
        right = compile_instruction_ir(bb, instr["right"], scope)
        return getattr(bb, op)(left, right)

    elif op in llvm_one_ops:
        value = compile_instruction_ir(bb, instr["value"], scope)
        return getattr(bb, op)(value)

    elif op in llvm_zero_ops:
        return getattr(bb, op)()

    elif op == "func_arg":
        return scope["ll_func"].args[ instr["value"] ]

    elif op == "alloca":
        ref = instr['ref']
        ptr = bb.alloca(ref["type"], name=ref["name"])
        scope['ptrs'][ref['id']] = ptr
        return ptr

    elif op == "store":
        ptr_id = instr['ref']['id']
        value = compile_instruction_ir(bb, instr['value'], scope)
        return bb.store(value, scope['ptrs'][ptr_id])

    elif op == "load":
        ptr_id = instr['ref']['id']
        return bb.load(scope['ptrs'][ptr_id])

    elif op == "const_val":
        return instr['value']

    else:
        raise BuildException("Unhandled operation type: " + op)


def numeric(is_int=True, bits=32):
    return {
        'is_primitive': True,
        'type': 'numeric',
        'is_int': is_int,
        'bits': bits }


_id_counter = 0
def next_id():
    global _id_counter
    _id_counter += 1
    return _id_counter


