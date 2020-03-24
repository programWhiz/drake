import sys
import llvmlite.ir as ll
from ctypes import *
from src.llvm_utils import run_llvm_code, create_binary_executable, compile_to_object_code


int8 = ll.IntType(8)
int32 = ll.IntType(32)
int64 = ll.IntType(64)

fntype = ll.FunctionType(ll.VoidType(), [])
module = ll.Module()

functype = ll.FunctionType(int32, [ll.PointerType(int8)], var_arg=True)
printf = module.declare_intrinsic('printf', [], functype)

func = ll.Function(module, fntype, name='foo')
bb_entry = func.append_basic_block()

builder = ll.IRBuilder()
builder.position_at_end(bb_entry)
bb = builder

str_count = 0

import string
keep_chars = set(ord(c) for c in string.ascii_letters + string.digits + string.punctuation + ' ')
str_escapes = { c: chr(c) if c in keep_chars else f"\\{c:02X}" for c in range(0, 255) }


def translate(s):
    return ''.join(str_escapes[c] for c in s)


def str_as_c_const(module:ll.Module, s : str):
    global str_count, str_escapes
    s = s.encode('utf-8')
    # length of bytes, plus 1 for null terminator
    s_len = len(s) + 1
    s = translate(s)
    s_chars = f'c"{s}\\00"'

    s_array_type = ll.ArrayType(int8, s_len)
    s_const = ll.FormattedConstant(s_array_type, s_chars)

    str_count += 1
    name = f'str.{str_count}'

    global_val = ll.GlobalVariable(module, s_array_type, name=name)
    global_val.global_constant = True
    global_val.unnamed_addr = True
    global_val.initializer = s_const

    return global_val


def gep_const_str(str_var):
    zero = ll.Constant(ll.IntType(32), 0)
    s_ptr = bb.gep(str_var, [zero], True)
    return bb.bitcast(s_ptr, ll.PointerType(int8))


s_const = str_as_c_const(module, "Hello From China: 你好!\n")
s_ptr = gep_const_str(s_const)
bb.call(printf, [ s_ptr ])

print(module)

