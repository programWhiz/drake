import llvmlite.ir as ll
import string

keep_chars = set(ord(c) for c in string.ascii_letters + string.digits + string.punctuation + ' ')

str_escapes = [ chr(c) if c in keep_chars else f"\\{c:02X}" for c in range(0, 255) ]

_string_id = 0


def next_str_id():
    global _string_id
    _string_id += 1
    return f'$str.{_string_id}'


def declare_str_const(module:ll.Module, s : str):
    global str_escapes
    s = s.encode('utf-8')
    # length of bytes, plus 1 for null terminator
    s_len = len(s) + 1
    s = ''.join(str_escapes[c] for c in s)
    s_chars = f'c"{s}\\00"'

    s_array_type = ll.ArrayType(ll.IntType(8), s_len)
    s_const = ll.FormattedConstant(s_array_type, s_chars)

    global_val = ll.GlobalVariable(module, s_array_type, name=next_str_id())
    global_val.global_constant = True
    global_val.unnamed_addr = True
    global_val.initializer = s_const

    return global_val


def gep_str_const(bb, str_var):
    zero = ll.Constant(ll.IntType(32), 0)
    s_ptr = bb.gep(str_var, [zero], True)  # x = &c[0]
    # return int8* (&c[0])
    return bb.bitcast(s_ptr, ll.PointerType(ll.IntType(8)))
