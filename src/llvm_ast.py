import llvmlite.ir as ll
from src.exceptions import *
from multimethod import isa, overload


def compile_module_ir(module):
    ll_mod = ll.Module(name=module["name"])
    scope = { 'module': module, 'll_module': ll_mod, 'classes': {} }

    for key, class_def in module.get("classes", { }).items():
        compile_class_ir(ll_mod, class_def, scope)

    for key, func in module.get("funcs", { }).items():
        compile_func_ir(ll_mod, func, scope)

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


def compile_func_ir(module, func, scope):
    arg_types = [arg["type"] for arg in func["args"]]
    fntype = ll.FunctionType(func["ret"]["type"], arg_types)
    ll_func = ll.Function(module, fntype, name=func["name"])
    block = ll_func.append_basic_block()
    bb = ll.IRBuilder()
    bb.position_at_end(block)

    scope = dict(scope)
    scope.update({ "func": func, "ll_func": ll_func, "ptrs": { } })

    for instr in func["instrs"]:
        compile_instruction_ir(bb, instr, scope)


def compile_class_ir(module, class_def, scope):
    ll_class = module.context.get_identified_type(class_def['name'])

    body_elems = [var['type'] for var in class_def['inst_vars']]
    ll_class.set_body(*body_elems)

    scope['classes'][class_def['id']] = { "class_def": class_def, "ll_class": ll_class }

    return ll_class


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

llvm_one_ops = { 'ret', 'not_', 'neg' }

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
    ref_type = instr.get('type', ref.get('type'))
    ref_type = get_alloc_type(ref_type, scope)
    ptr = bb.alloca(ref_type, name=ref["name"])
    scope['ptrs'][ref['id']] = ptr
    return ptr


def get_alloc_type(ref_type, scope: dict):
    if isinstance(ref_type, ll.Type):
        return ref_type   # already compiled LLVM type

    # TODO: handle smart_ptr
    assert ref_type['type'] == 'ptr'
    class_id = ref_type['class']['id']
    return scope['classes'][class_id]['ll_class']


@overload
def compile_instruction_ir(bb, instr: is_op("gep"), scope: dict):
    ptr_id = instr['ref']['id']
    ptr = scope['ptrs'][ptr_id]

    if isinstance(instr['value'], dict):
        value = compile_instruction_ir(bb, instr['value'], scope)
    elif isinstance(instr['value'], int):
        value = ll.Constant(ll.IntType(32), instr['value'])

    # TODO: toggle with config option?
    zero = ll.Constant(ll.IntType(32), 0)
    return bb.gep(ptr, [zero, value], inbounds=True)


@overload
def compile_instruction_ir(bb, instr: is_op("store"), scope: dict):
    ref = instr['ref']

    if 'op' in ref:
        ptr_id = compile_instruction_ir(bb, ref, scope)
    elif 'id' in ref:
        ptr_id = scope['ptrs'][ref['id']]
    else:
        raise BuildException("Expected store.ref to be pointer id or instruction")

    value = compile_instruction_ir(bb, instr['value'], scope)
    return bb.store(value, ptr_id)


@overload
def compile_instruction_ir(bb, instr: is_op("load"), scope: dict):
    ref = instr['ref']

    if 'op' in ref:
        ptr_id = compile_instruction_ir(bb, ref, scope)
    elif 'id' in ref:
        ptr_id = scope['ptrs'][ref['id']]
    else:
        raise Exception("Expected load.ref to be id or instruction")

    return bb.load(ptr_id)


@overload
def compile_instruction_ir(bb, instr: is_op("const_val"), scope: dict):
    return instr['value']


@overload
def compile_instruction_ir(bb, instr: is_op("if"), scope: dict):
    cond = compile_instruction_ir(bb, instr['cond'], scope)
    tblock = bb.append_basic_block()
    exit_blk = bb.append_basic_block()

    false_instrs = instr.get('false')
    if false_instrs:
        fblock = bb.append_basic_block()
    else:
        fblock = exit_blk

    bb.cbranch(cond, tblock, fblock)

    bb.position_at_end(tblock)
    for true_instr in instr['true']:
        compile_instruction_ir(bb, true_instr, scope)
    bb.branch(exit_blk)

    if false_instrs:
        bb.position_at_end(fblock)
        for false_instr in false_instrs:
            compile_instruction_ir(bb, false_instr, scope)
        bb.branch(exit_blk)

    bb.position_at_end(exit_blk)


@overload
def compile_instruction_ir(bb, instr: is_op("loop"), scope: dict):
    check_cond = bb.append_basic_block()
    body = bb.append_basic_block()
    exit_blk = bb.append_basic_block()

    # begin the loop
    bb.branch(check_cond)

    # Loop condition, jump to body or end
    bb.position_at_end(check_cond)
    cond = compile_instruction_ir(bb, instr['cond'], scope)
    bb.cbranch(cond, body, exit_blk)

    # Body, run set of body instructions
    bb.position_at_end(body)
    for body_instr in instr['body']:
        compile_instruction_ir(bb, body_instr, scope)
    bb.branch(check_cond)  # retry loop condition

    # Exit loop
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
