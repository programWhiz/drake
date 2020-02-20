import math
import pytest
import llvmlite.ir as ll
from ctypes import CFUNCTYPE, c_double, c_int32, c_int8, c_int16, c_int64, c_float, c_longdouble
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
        "funcs": { func_def['id']: func_def }
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
        "funcs": { func_def['id']: func_def }
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
        "funcs": { func_def['id']: func_def }
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
        "funcs": { func_def['id']: func_def }
    })

    expect = 2 * 3.1415

    cfunc_type = CFUNCTYPE(c_float)
    result = run_ir_code(module, "test_func", cfunc_type, [])
    assert math.isclose(expect, result, abs_tol=0.001)
