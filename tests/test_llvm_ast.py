import math
import pytest
import llvmlite.ir as ll
from ctypes import CFUNCTYPE, c_int32, c_int8, c_float, c_uint32, c_int64, c_int16, c_double
from src.llvm_utils import run_ir_code
from src.llvm_ast import compile_module_ir, next_id


def test_binary_ops_int32():
    _test_ir_binary_op_int32("add", 14, 26, 14 + 26)
    _test_ir_binary_op_int32("sub", 14, 26, 14 - 26)
    _test_ir_binary_op_int32("mul", 14, 26, 14 * 26)
    _test_ir_binary_op_int32("sdiv", 200, 12, 200 // 12)


def test_binary_ops_float32():
    _test_ir_binary_op_float32("fadd", 14.5, 26.4, 14.5 + 26.4)
    _test_ir_binary_op_float32("fsub", 14.5, 26.4, 14.5 - 26.4)
    _test_ir_binary_op_float32("fmul", 14.5, 26.4, 14.5 * 26.4)
    _test_ir_binary_op_float32("fdiv", 200.12, 12.07, 200.12 / 12.07)


def _test_ir_binary_op_int32(op_name, left_val, right_val, expect):
    int_type = ll.IntType(32)
    a = { "name": "a", "id": next_id(), "type": int_type }
    b = { "name": "b", "id": next_id(), "type": int_type }
    ret = { "name": "ret", "id": next_id(), "type": int_type }

    func_def = {
        "name": op_name,
        "id": next_id(),
        "ret": ret,
        "args": [ a, b ],
        "instrs": [
            {
                "op": "ret",
                "value": {
                    "op": op_name,
                    "left": { "op": "func_arg", "value": 0 },
                    "right": { "op": "func_arg", "value": 1 } }
            },
        ]
    }

    module = {
        "name": "test_" + op_name,
        "funcs": [ func_def ]
    }

    module = compile_module_ir(module)

    cfunc_type = CFUNCTYPE(c_int32, c_int32, c_int32)
    result = run_ir_code(module, op_name, cfunc_type, [ left_val, right_val ])
    assert expect == result


def _test_ir_binary_op_float32(op_name, left_val, right_val, expect):
    float_type = ll.FloatType()
    a = { "name": "a", "id": next_id(), "type": float_type }
    b = { "name": "b", "id": next_id(), "type": float_type }
    ret = { "name": "ret", "id": next_id(), "type": float_type }

    func_def = {
        "name": op_name,
        "id": next_id(),
        "ret": ret,
        "args": [ a, b ],
        "instrs": [
            {
                "op": "ret",
                "value": {
                    "op": op_name,
                    "left": { "op": "func_arg", "value": 0 },
                    "right": { "op": "func_arg", "value": 1 } }
            },
        ]
    }

    module = {
        "name": "test_" + op_name,
        "funcs": [ func_def ]
    }

    module = compile_module_ir(module)

    cfunc_type = CFUNCTYPE(c_float, c_float, c_float)
    result = run_ir_code(module, op_name, cfunc_type, [ left_val, right_val ])
    assert math.isclose(expect, result, abs_tol=0.001)


def test_intermediate_var():
    float_type = ll.FloatType()
    a = { "name": "a", "id": next_id(), "type": float_type }
    b = { "name": "b", "id": next_id(), "type": float_type }
    c = { "name": "c", "id": next_id(), "type": float_type }
    d = { "name": "d", "id": next_id(), "type": float_type }
    ret = { "name": "ret", "id": next_id(), "type": float_type }

    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [ a, b ],
        "instrs": [
            # declare c and d
            { "op": "alloca", "ref": c },
            { "op": "alloca", "ref": d },
            # c = a + b
            {
                "op": "store",
                "ref": c,
                "value": {
                    "op": "fadd",
                    "left": { "op": "func_arg", "value": 0 },
                    "right": { "op": "func_arg", "value": 1 }
                }
            },
            # d = a * b
            {
                "op": "store",
                "ref": d,
                "value": {
                    "op": "fmul",
                    "left": { "op": "func_arg", "value": 0 },
                    "right": { "op": "func_arg", "value": 1 }
                }
            },
            # return d - c
            {
                "op": "ret",
                "value": {
                    "op": "fsub",
                    "left": { "op": "load", "ref": d },
                    "right": { "op": "load", "ref": c }
                }
            },
        ]
    }

    module = {
        "name": "test_store",
        "funcs": [ func_def ]
    }

    module = compile_module_ir(module)

    # Replicate the logic in python
    A, B = 3.4, 5.7
    C, D = A + B, A * B
    expect = D - C

    cfunc_type = CFUNCTYPE(c_float, c_float, c_float)
    result = run_ir_code(module, "test_func", cfunc_type, [ A, B ])
    assert math.isclose(expect, result, abs_tol=0.001)


def test_constants():
    float_type = ll.FloatType()
    ret = { "name": "ret", "id": next_id(), "type": float_type }

    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [],
        "instrs": [
            {
                "op": "ret",
                "value": {
                    "op": "fmul",
                    "left": { "op": "const_val", "value": ll.Constant(float_type, 3.1415) },
                    "right": { "op": "const_val", "value": ll.Constant(float_type, 2.0) }
                }
            }
        ]
    }

    module = compile_module_ir({
        "name": "test_store",
        "funcs": [ func_def ]
    })

    expect = 2 * 3.1415

    cfunc_type = CFUNCTYPE(c_float)
    result = run_ir_code(module, "test_func", cfunc_type, [])
    assert math.isclose(expect, result, abs_tol=0.001)


def test_bool_ops():
    import operator

    for opname in ('and_', 'or_', 'xor'):
        for a in (True, False):
            for b in (True, False):
                op_func = getattr(operator, opname)
                _test_bool_op(a, b, opname, expect=op_func(a, b))


def _test_bool_op(A, B, opname, expect):
    bool_type = ll.IntType(8)
    a = { "name": "a", "id": next_id(), "type": bool_type }
    b = { "name": "b", "id": next_id(), "type": bool_type }
    ret = { "name": "ret", "id": next_id(), "type": bool_type }

    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [a, b],
        "instrs": [
            {
                "op": "ret",
                "value": {
                    "op": opname,
                    "left": { "op": "func_arg", "value": 0 },
                    "right": { "op": "func_arg", "value": 1 },
                }
            }
        ]
    }

    module = compile_module_ir({
        "name": "test",
        "funcs": [ func_def ]
    })

    cfunc_type = CFUNCTYPE(c_int8, c_int8, c_int8)
    result = run_ir_code(module, "test_func", cfunc_type, [A, B])
    result = (result == 1)  # cast from int to bool
    assert result == expect


def test_boolean_not():
    bool_type = ll.IntType(1)
    a = { "name": "a", "id": next_id(), "type": bool_type }
    ret = { "name": "ret", "id": next_id(), "type": bool_type }

    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [a],
        "instrs": [
            {
                "op": "ret",
                "value": {
                    "op": "s!=",
                    "left": { "op": "func_arg", "value": 0 },
                    "right": { "op": "const_val", "value": ll.Constant(bool_type, 1) },
                }
            }
        ]
    }

    module = compile_module_ir({
        "name": "test", "funcs": [ func_def ]
    })

    cfunc_type = CFUNCTYPE(c_int8, c_int8)

    for func_arg in (True, False):
        result = run_ir_code(module, "test_func", cfunc_type, [func_arg])
        result = (result != 0)  # cast from int to bool
        assert result == (not func_arg)


def test_comparisons():
    a, b = 3.5, 4.6
    args = ll.FloatType(), c_float
    _test_comparisons(a, b, a != b, "f!=", *args)
    _test_comparisons(a, a, a != a, "f!=", *args)
    _test_comparisons(a, b, a == b, "f==", *args)
    _test_comparisons(a, a, a == a, "f==", *args)
    _test_comparisons(a, b, a > b, "f>", *args)
    _test_comparisons(a, b, a >= b, "f>=", *args)
    _test_comparisons(a, b, a < b, "f<", *args)
    _test_comparisons(a, b, a <= b, "f<=", *args)

    a, b = 7, 6
    args = ll.IntType(32), c_int32
    _test_comparisons(a, b, a != b, "s!=", *args)
    _test_comparisons(a, a, a != a, "s!=", *args)
    _test_comparisons(a, b, a == b, "s==", *args)
    _test_comparisons(a, a, a == a, "s==", *args)
    _test_comparisons(a, b, a > b, "s>", *args)
    _test_comparisons(a, b, a >= b, "s>=", *args)
    _test_comparisons(a, b, a < b, "s<", *args)
    _test_comparisons(a, b, a <= b, "s<=", *args)

    # Test unsigned, should be same as signed in this case
    args = ll.IntType(32), c_uint32
    _test_comparisons(a, b, a != b, "u!=", *args)
    _test_comparisons(a, a, a != a, "u!=", *args)
    _test_comparisons(a, b, a == b, "u==", *args)
    _test_comparisons(a, a, a == a, "u==", *args)
    _test_comparisons(a, b, a > b, "u>", *args)
    _test_comparisons(a, b, a >= b, "u>=", *args)
    _test_comparisons(a, b, a < b, "u<", *args)
    _test_comparisons(a, b, a <= b, "u<=", *args)

    # Test with negs, should reverse equality
    a, b = 4, -7
    args = ll.IntType(32), c_uint32
    _test_comparisons(a, b, a != b, "u!=", *args)
    _test_comparisons(a, a, a != a, "u!=", *args)
    _test_comparisons(a, b, a == b, "u==", *args)
    _test_comparisons(a, a, a == a, "u==", *args)
    _test_comparisons(a, b, a < b, "u>", *args)
    _test_comparisons(a, b, a < b, "u>=", *args)
    _test_comparisons(a, b, a > b, "u<", *args)
    _test_comparisons(a, b, a > b, "u<=", *args)


def _test_comparisons(A, B, expect, opname, arg_type, c_arg_type):
    bool_type = ll.IntType(1)
    a = { "name": "a", "id": next_id(), "type": arg_type }
    b = { "name": "b", "id": next_id(), "type": arg_type }
    ret = { "name": "ret", "id": next_id(), "type": bool_type }

    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [a, b],
        "instrs": [
            {
                "op": "ret",
                "value": {
                    "op": opname,
                    "left": { "op": "func_arg", "value": 0 },
                    "right": { "op": "func_arg", "value": 1 },
                }
            }
        ]
    }

    module = compile_module_ir({
        "name": "test", "funcs": [ func_def ]
    })

    cfunc_type = CFUNCTYPE(c_int8, c_arg_type, c_arg_type)

    result = run_ir_code(module, "test_func", cfunc_type, [A, B])
    result = (result != 0)  # cast from int to bool
    assert result == expect


def test_if_else_block():
    int_type = ll.IntType(32)
    a = { "name": "a", "id": next_id(), "type": int_type }
    b = { "name": "b", "id": next_id(), "type": int_type }
    c = { "name": "c", "id": next_id(), "type": int_type }
    ret = { "name": "ret", "id": next_id(), "type": int_type }

    # define function: a if a > b else b
    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [a, b],
        "instrs": [
            { "op": "alloca", "ref": c },
            {
                "op": "if",
                "cond": {
                    "op": "s>",
                    "left": { "op": "func_arg", "value": 0 },
                    "right": { "op": "func_arg", "value": 1 },
                },
                "true": [{
                    "op": "store",
                    "ref": c,
                    "value": { "op": "func_arg", "value": 0 },
                }],
                "false": [{
                    "op": "store",
                    "ref": c,
                    "value": { "op": "func_arg", "value": 1 },
                }]
            },
            # return c
            { "op": "ret", "value": { "op": "load", "ref": c } }
        ]
    }

    module = compile_module_ir({
        "name": "test", "funcs": [ func_def ]
    })

    cfunc_type = CFUNCTYPE(c_int32, c_int32, c_int32)

    for a in (1, -4, 10, 3, 12):
        for b in (7, -1, 0, 8, 20):
            result = run_ir_code(module, "test_func", cfunc_type, [a, b])
            expect = a if a > b else b
            assert result == expect


def test_if_block():
    int_type = ll.IntType(32)
    a = { "name": "a", "id": next_id(), "type": int_type }
    b = { "name": "b", "id": next_id(), "type": int_type }
    c = { "name": "c", "id": next_id(), "type": int_type }
    ret = { "name": "ret", "id": next_id(), "type": int_type }

    # define function: a if a > b else b
    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [a, b],
        "instrs": [
            { "op": "alloca", "ref": c },
            # c = a
            { "op": "store", "ref": c, "value": { "op": "func_arg", "value": 0 } },
            # if b > a: c = b;
            {
                "op": "if",
                "cond": {
                    "op": "s>",
                    "left": { "op": "func_arg", "value": 1 },
                    "right": { "op": "func_arg", "value": 0 },
                },
                "true": [{
                    "op": "store",
                    "ref": c,
                    "value": { "op": "func_arg", "value": 1 },
                }]
            },
            # return c
            { "op": "ret", "value": { "op": "load", "ref": c } }
        ]
    }

    module = compile_module_ir({
        "name": "test", "funcs": [ func_def ]
    })

    cfunc_type = CFUNCTYPE(c_int32, c_int32, c_int32)

    def expect(a, b):
        c = a
        if b > a:
            c = b
        return c

    for a in (1, -4, 10, 4, 3, 12):
        for b in (7, -1, 0, 4, 8, 20):
            result = run_ir_code(module, "test_func", cfunc_type, [a, b])
            assert result == expect(a, b)


def test_loop():
    int_type = ll.IntType(32)
    a = { "name": "a", "id": next_id(), "type": int_type }
    c = { "name": "c", "id": next_id(), "type": int_type }
    i = { "name": "i", "id": next_id(), "type": int_type }
    ret = { "name": "ret", "id": next_id(), "type": int_type }

    # def func(a):
    #   b = 0
    #   while i < a:
    #       b += 2
    #       i += 1
    #   return c
    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [a],
        "instrs": [
            # c = 0
            { "op": "alloca", "ref": c },
            { "op": "store", "ref": c, "value": { "op": "const_val", "value": ll.Constant(int_type, 0) } },
            # i = 0
            { "op": "alloca", "ref": i },
            { "op": "store", "ref": i, "value": { "op": "const_val", "value": ll.Constant(int_type, 0) } },
            # if b > a: c = b;
            {
                "op": "loop",
                # i < a
                "cond": {
                    "op": "s<",
                    "left": { "op": "load", "ref": i },
                    "right": { "op": "func_arg", "value": 0 },
                },
                "body": [
                    # c += 2
                    {
                        "op": "store",
                        "ref": c,
                        "value": {
                            "op": "add",
                            "left": { "op": "load", "ref": c },
                            "right": { "op": "const_val", "value": ll.Constant(int_type, 2) },
                        }
                    },
                    # i += 1
                    {
                        "op": "store",
                        "ref": i,
                        "value": {
                            "op": "add",
                            "left": { "op": "load", "ref": i },
                            "right": { "op": "const_val", "value": ll.Constant(int_type, 1) },
                        }
                    },
                ],
            },
            # return c
            { "op": "ret", "value": { "op": "load", "ref": c } }
        ]
    }

    module = compile_module_ir({
        "name": "test", "funcs": [ func_def ]
    })

    cfunc_type = CFUNCTYPE(c_int32, c_int32)

    for a in (1, 10, 4, 3, 12, 0, -1):
        result = run_ir_code(module, "test_func", cfunc_type, [a])
        assert result == max(2 * a, 0)


def test_class():
    int_type = ll.IntType(32)

    pair_class = {
        "name": "Pair_i32",
        "type": "class",
        "id": next_id(),
        "inst_vars": [
            { "name": "a", "id": next_id(), "type": int_type },
            { "name": "b", "id": next_id(), "type": int_type },
        ]
    }

    pair = { "name": "pair", "id": next_id(), "type": pair_class }
    ret = { "name": "ret", "id": next_id(), "type": int_type }

    # return pair.a if a > 0 else pair.b
    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [],
        "instrs": [
            # define "pair"
            {
              "op": "alloca",
              "ref": pair,
              "type": { "type": "ptr", "class": pair_class }
            },
            # pair.a = 42
            {
                "op": "store",
                "ref": { "op": "gep", "ref": pair, "value": [ 0, 0 ] },
                "value": { "op": "const_val", "value": ll.Constant(int_type, 42) }
            },
            # pair.b = -3
            {
                "op": "store",
                "ref": { "op": "gep", "ref": pair, "value": [ 0, 1 ] },
                "value": { "op": "const_val", "value": ll.Constant(int_type, -3) }
            },
            # return pair.a
            {
                "op": "ret",
                "value": {
                    "op": "load", "ref": { "op": "gep", "ref": pair, "value": [ 0, 0 ] }
                }
            }
        ]
    }

    module = compile_module_ir({
        "name": "test",
        "classes": [ pair_class ],
        "funcs": [ func_def ]
    })

    cfunc_type = CFUNCTYPE(c_int32)

    result = run_ir_code(module, "test_func", cfunc_type, [1])
    assert result == 42


def test_sizeof():
    _test_sizeof(ll.IntType(8), c_int8, 1)
    _test_sizeof(ll.IntType(16), c_int16, 2)
    _test_sizeof(ll.IntType(32), c_int32, 4)
    _test_sizeof(ll.IntType(64), c_int64, 8)
    _test_sizeof(ll.FloatType(), c_float, 4)
    _test_sizeof(ll.DoubleType(), c_double, 8)


def _test_sizeof(ll_type, c_type, expect_size):
    int_type = ll.IntType(64)
    arg1 = { "name": "arg1", "id": next_id(), "type": ll_type }
    ret = { "name": "ret", "id": next_id(), "type": int_type }

    # return pair.a if a > 0 else pair.b
    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [ arg1 ],
        "instrs": [{
            "op": "ret",
            "value": {
                "op": "sizeof",
                "ref": { "op": "func_arg", "value": 0 }
            }
        }]
    }

    module = compile_module_ir({ "name": "test", "funcs": [ func_def ] })
    print(module)

    cfunc_type = CFUNCTYPE(c_int64, c_type)
    result = run_ir_code(module, "test_func", cfunc_type, [ 0 ])
    assert result == expect_size


def test_malloc_free_single_int():
    int_type = ll.IntType(32)

    my_ptr = { "name": "my_ptr", "id": next_id(), "type": int_type }
    temp_var = { "name": "temp_var", "id": next_id(), "type": int_type }
    ret = { "name": "ret", "id": next_id(), "type": int_type }

    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [],
        "instrs": [
            # my_ptr = new int[1];
            { "op": "malloc", "ref": my_ptr },
            # *my_ptr = 32
            {
              "op": "store",
              "ref": my_ptr,
              "value": { "op": "const_val", "value": ll.Constant(int_type, 32) }
            },
            # int temp_var = my_ptr[0];
            { "op": "alloca", "ref": temp_var },
            {
                "op": "store",
                "ref": temp_var,
                "value": {
                    "op": "load",
                    "ref": my_ptr,
                }
            },
            # free(my_ptr)
            { "op": "free", "ref": my_ptr },
            # return temp_var
            { "op": "ret", "value": { "op": "load", "ref": temp_var } }
        ]
    }

    module = compile_module_ir({ "name": "test", "funcs": [ func_def ] })
    print(module)

    cfunc_type = CFUNCTYPE(c_int32)

    result = run_ir_code(module, "test_func", cfunc_type, [])
    assert result == 32


def test_malloc_free_int_array():
    int_type = ll.IntType(32)

    my_ptr = { "name": "my_ptr", "id": next_id(), "type": int_type, "count": 10 }
    temp_var = { "name": "temp_var", "id": next_id(), "type": int_type }
    ret = { "name": "ret", "id": next_id(), "type": int_type }

    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [],
        "instrs": [
            # my_ptr = new int[10];
            { "op": "malloc", "ref": my_ptr },
            # my_ptr[5] = 32
            {
                "op": "store",
                "ref": {
                    "op": "gep",
                    "ref": my_ptr,
                    "value": 5
                },
                "value": { "op": "const_val", "value": ll.Constant(int_type, 32) }
            },
            # int temp_var = my_ptr[5];
            { "op": "alloca", "ref": temp_var },
            {
                "op": "store",
                "ref": temp_var,
                "value": {
                    "op": "load",
                    "ref": {
                        "op": "gep",
                        "ref": my_ptr,
                        "value": 5
                    }
                }
            },
            # free(my_ptr)
            { "op": "free", "ref": my_ptr },
            # return temp_var
            { "op": "ret", "value": { "op": "load", "ref": temp_var } }
        ]
    }

    module = compile_module_ir({ "name": "test", "funcs": [ func_def ] })
    print(module)

    cfunc_type = CFUNCTYPE(c_int32)

    result = run_ir_code(module, "test_func", cfunc_type, [])
    assert result == 32


def test_alloc_array():
    int_type = ll.IntType(32)

    my_ptr = { "name": "my_ptr", "id": next_id(), "type": int_type, "count": 10 }
    ret = { "name": "ret", "id": next_id(), "type": int_type }

    func_def = {
        "name": "test_func",
        "id": next_id(),
        "ret": ret,
        "args": [],
        "instrs": [
            # my_ptr = new int[10];
            { "op": "alloca", "ref": my_ptr },
            # my_ptr[5] = 32
            {
                "op": "store",
                "ref": {
                    "op": "gep",
                    "ref": my_ptr,
                    "value": 5
                },
                "value": { "op": "const_val", "value": ll.Constant(int_type, 32) }
            },
            # return my_ptr[5]
            {
                "op": "ret",
                "value": {
                    "op": "load",
                    "ref": { "op": "gep", "ref": my_ptr, "value": 5 }
                }
            }
        ]
    }

    module = compile_module_ir({ "name": "test", "funcs": [ func_def ] })
    print(module)

    cfunc_type = CFUNCTYPE(c_int32)

    result = run_ir_code(module, "test_func", cfunc_type, [])
    assert result == 32


def test_call_func():
    int_type = ll.IntType(32)
    ret = { "name": "ret", "id": next_id(), "type": int_type }

    inner_func = {
        "name": "inner_func",
        "id": next_id(), "ret": ret, "args": [], "instrs": [
            { "op": "ret", "value": { "op": "const_val", "value": ll.Constant(int_type, 32) } }
        ]
    }

    outer_func = {
        "name": "outer_func",
        "id": next_id(), "ret": ret, "args": [], "instrs": [
            {
                "op": "ret",
                "value": { "op": "call", "func": inner_func, "args": [] }
            }
        ]
    }

    module = compile_module_ir({
        "name": "test",
        "funcs": [ inner_func, outer_func ]
    })
    print(module)

    cfunc_type = CFUNCTYPE(c_int32)

    result = run_ir_code(module, "outer_func", cfunc_type, [])
    assert result == 32
