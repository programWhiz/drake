import sys
from collections import OrderedDict

import llvmlite.ir as ll
from src.exceptions import *
from multimethod import isa, overload

from src.llvm_string import declare_str_const, gep_str_const


def compile_module_ir(module):
    ll_mod = ll.Module(name=module["name"])

    scope = {
        'module': module,
        'll_module': ll_mod,
        'classes': OrderedDict(),
        'funcs': OrderedDict(),
        'intrinsics': compile_module_intrinsics(ll_mod),
    }

    for class_def in module.get("classes", []):
        compile_class_ir(ll_mod, class_def, scope)

    for func in module.get("funcs", []):
        compile_func_ir(ll_mod, func, scope)

    return ll_mod


def compile_module_intrinsics(module) -> dict:
    void_type = ll.VoidType()
    byte_ptr = ll.PointerType(ll.IntType(8))
    i32 = ll.IntType(32)
    i64 = ll.IntType(64)

    intrinsics = {}
    def decl(name, *args, **kwargs):
        functype = ll.FunctionType(*args, **kwargs)
        intrinsics[name] = module.declare_intrinsic(name, [], functype)

    decl('malloc', byte_ptr, [i64])
    decl('free', void_type, [byte_ptr])
    decl('printf', i32, [ byte_ptr ], var_arg=True)
    decl('printf_s', i32, [ byte_ptr, i32 ], var_arg=True)
    decl('sprintf', i32, [ byte_ptr, byte_ptr ], var_arg=True)
    decl('sprintf_s', i32, [ byte_ptr, i32, byte_ptr ], var_arg=True)
    decl('snprintf', i32, [ byte_ptr, i32, byte_ptr ], var_arg=True)

    return intrinsics


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

    scope['funcs'][ func['id'] ] = ll_func


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
    count = get_alloc_count(bb, instr, scope) or 1
    ptr = bb.alloca(ref_type, name=ref["name"], size=count)
    scope['ptrs'][ref['id']] = ptr
    return ptr


def sizeof_i32(bb, ir_type):
    null_ptr = ll.Constant(ll.PointerType(ir_type), 'null')
    size = bb.gep(null_ptr, [ ll.Constant(ll.IntType(32), 1) ], inbounds=False)
    size = bb.ptrtoint(size, ll.IntType(32))
    return size


def sizeof_i64(bb, ir_type):
    size32 = sizeof_i32(bb, ir_type)
    return bb.zext(size32, ll.IntType(64))


@overload
def compile_instruction_ir(bb, instr: is_op("sizeof"), scope: dict):
    ref = instr['ref']
    if 'op' in ref:
        ref = compile_instruction_ir(bb, ref, scope)
        ref_type = ref.type
    else:
        ref_type = instr.get('type', ref.get('type'))

    ref_type = get_alloc_type(ref_type, scope)
    return sizeof_i64(bb, ref_type)


def get_alloc_count(bb, instr, scope):
    count = instr.get('count', instr['ref'].get('count'))
    if count is None:
        return

    if isinstance(count, dict):   # instruction
        return compile_instruction_ir(bb, count, scope)
    if isinstance(count, int):
        # A count of one is just a pointer
        if count == 1:
            return None
        return ll.Constant(ll.IntType(64), count)
    elif isinstance(count, ll.IntType):
        return count

    print("Allocation `count` must be int, ll.IntType, or instruction. Found:", count, file=sys.stdout)
    raise BuildException("Allocation `count` must be int, ll.IntType, or instruction.")


@overload
def compile_instruction_ir(bb, instr: is_op("malloc"), scope: dict):
    ref = instr['ref']
    ref_type = instr.get('type', ref.get('type'))
    ref_type = get_alloc_type(ref_type, scope)
    size_bytes = sizeof_i64(bb, ref_type)

    count = get_alloc_count(bb, instr, scope)
    if count:
        # TODO: use _with_overflow based on config?
        size_bytes = bb.mul(size_bytes, count)

    malloc_func = scope['intrinsics']['malloc']
    byte_ptr = bb.call(malloc_func, [ size_bytes ], name=ref["name"])
    ptr = bb.bitcast(byte_ptr, ll.PointerType(ref_type))

    scope['ptrs'][ref['id']] = ptr
    return ptr


@overload
def compile_instruction_ir(bb, instr: is_op("free"), scope: dict):
    ref = instr['ref']

    ptr = scope['ptrs'].pop(ref['id'])
    byte_ptr = bb.bitcast(ptr, ll.PointerType(ll.IntType(8)))

    free_func = scope['intrinsics']['free']
    call_result = bb.call(free_func, [ byte_ptr ], name=ref["name"])
    return call_result


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

    values = instr.get('value')
    if values is None:
        print('Missing `value` key in `gep` instruction: ', instr, file=sys.stderr)
        raise BuildException('Missing `value` key in `gep` instruction.')

    if not isinstance(values, (list, tuple)):
        values = [ values ]

    addr_values = []
    for value in values:
        if isinstance(value, dict):
            addr_value = compile_instruction_ir(bb, value, scope)
        elif isinstance(value, int):
            addr_value = ll.Constant(ll.IntType(32), value)
        elif isinstance(value, ll.Type):
            addr_value = value
        else:
            print(f"Address values in `gep` should be instruction or integer constant. Found:", value, file=sys.stderr)
            raise BuildException(f"Address values in `gep` should be instruction or integer constant.")

        addr_values.append(addr_value)

    return bb.gep(ptr, addr_values, inbounds=True)


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
def compile_instruction_ir(bb, instr: is_op("const_str"), scope: dict):
    s_const = declare_str_const(scope['ll_module'], instr['value'])
    return gep_str_const(bb, s_const)


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


@overload
def compile_instruction_ir(bb, instr: is_op("call"), scope: dict):
    intrinsic_name = instr.get('intrinsic')
    if intrinsic_name:
        func_ptr = scope['intrinsics'][intrinsic_name]
    else:  # not an intrinsic function
        func_ptr = instr['func']
        # Is it already a function pointer?
        if not isinstance(func_ptr, ll.Function):
            func_id = func_ptr['id']
            func_ptr = scope['funcs'][func_id]

    args = [ compile_instruction_ir(bb, arg, scope) for arg in instr['args'] ]
    return bb.call(func_ptr, args)


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
