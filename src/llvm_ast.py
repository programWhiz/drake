import llvmlite.ir as ll
from src.exceptions import *
from multimethod import isa, overload


def compile_module_ir(module):
    ll_mod = ll.Module(name=module["name"])
    for key, func in module.get("funcs", { }).items():
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
    arg_types = [arg["type"] for arg in func["args"]]
    fntype = ll.FunctionType(func["ret"]["type"], arg_types)
    ll_func = ll.Function(module, fntype, name=func["name"])
    block = ll_func.append_basic_block()
    bb = ll.IRBuilder()
    bb.position_at_end(block)

    scope = { "module": module, "func": func, "ll_func": ll_func, "ptrs": { } }
    for instr in func["instrs"]:
        compile_instruction_ir(bb, instr, scope)


llvm_binary_ops = {
    'add', 'fadd', 'sub', 'fsub', 'mul', 'fmul', 'sdiv', 'udiv', 'fdiv', 'and_', 'or_', 'xor',
    'fabs', 'srem', 'urem', 'frem', 'shl', 'lshr', 'ashr',
}

llvm_comparison = {
    'f<', 'f<=', 'f!=', 'f==', 'f>=', 'f>',
    's<', 's<=', 's!=', 's==', 's>=', 's>',
    'u<', 'u<=', 'u!=', 'u==', 'u>=', 'u>',
}

llvm_zero_ops = { 'ret_void' }

llvm_one_ops = { 'ret', 'not_','neg' }

is_binary_op = lambda x: x['op'] in llvm_binary_ops
is_zero_op = lambda x: x['op'] in llvm_zero_ops
is_single_op = lambda x: x['op'] in llvm_one_ops
is_comparison = lambda x: x['op'] in llvm_comparison


def is_op(op_name):
    return lambda x: x['op'] == op_name


@overload
def compile_instruction_ir(bb, instr, scope: dict):
    raise BuildException("Unhandled operation type: " + instr['op'])


@overload
def compile_instruction_ir(bb, instr: is_binary_op, scope: dict):
    left = compile_instruction_ir(bb, instr["left"], scope)
    right = compile_instruction_ir(bb, instr["right"], scope)
    return getattr(bb, instr['op'])(left, right)


@overload
def compile_instruction_ir(bb, instr: is_comparison, scope: dict):
    left = compile_instruction_ir(bb, instr["left"], scope)
    right = compile_instruction_ir(bb, instr["right"], scope)

    op = instr['op']
    data_type, cmp = op[0], op[1:]

    if data_type == 'f':
        # Using unordered because either op can be NaN
        return bb.fcmp_unordered(cmp, left, right)
    elif data_type == 's':
        return bb.icmp_signed(cmp, left, right)
    elif data_type == 'u':
        return bb.icmp_unsigned(cmp, left, right)


@overload
def compile_instruction_ir(bb, instr: is_single_op, scope: dict):
    value = compile_instruction_ir(bb, instr["value"], scope)
    return getattr(bb, instr['op'])(value)


@overload
def compile_instruction_ir(bb, instr: is_zero_op, scope: dict):
    return getattr(bb, instr['op'])()


@overload
def compile_instruction_ir(bb, instr: is_op("func_arg"), scope: dict):
    return scope["ll_func"].args[instr["value"]]


@overload
def compile_instruction_ir(bb, instr: is_op("alloca"), scope: dict):
    ref = instr['ref']
    ptr = bb.alloca(ref["type"], name=ref["name"])
    scope['ptrs'][ref['id']] = ptr
    return ptr


@overload
def compile_instruction_ir(bb, instr: is_op("store"), scope: dict):
    ptr_id = instr['ref']['id']
    value = compile_instruction_ir(bb, instr['value'], scope)
    return bb.store(value, scope['ptrs'][ptr_id])


@overload
def compile_instruction_ir(bb, instr: is_op("load"), scope: dict):
    ptr_id = instr['ref']['id']
    return bb.load(scope['ptrs'][ptr_id])


@overload
def compile_instruction_ir(bb, instr: is_op("const_val"), scope: dict):
    return instr['value']

@overload
def compile_instruction_ir(bb, instr: is_op("if"), scope: dict):
    cond = compile_instruction_ir(bb, instr['cond'], scope)
    tblock = bb.append_basic_block()
    exit_blk = bb.append_basic_block()

    false_instr = instr.get('false')
    if false_instr:
        fblock = bb.append_basic_block()
    else:
        fblock = exit_blk

    bb.cbranch(cond, tblock, fblock)

    bb.position_at_end(tblock)
    compile_instruction_ir(bb, instr['true'], scope)
    bb.branch(exit_blk)

    if false_instr:
        bb.position_at_end(fblock)
        compile_instruction_ir(bb, false_instr, scope)
        bb.branch(exit_blk)

    bb.position_at_end(exit_blk)


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
