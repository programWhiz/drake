import math

from .test_base import get_test_stdout
from src.hl_ast import *


def test_add_literals_1():
    _test_binary_literals(3, 5, BinaryAdd, 8)


def test_add_literals_2():
    _test_binary_literals(0, 0, BinaryAdd, 0)


def test_add_literals_3():
    _test_binary_literals(-5, 10, BinaryAdd, 5)


def test_add_literals_4():
    _test_binary_literals(5.5, 1.2, BinaryAdd, 5.5 + 1.2)


def test_add_literals_5():
    _test_binary_literals(-3.1415, 7.0, BinaryAdd, -3.1415 + 7.0)


def test_sub_literals_1():
    _test_binary_literals(3, 5, BinarySub, -2)


def test_sub_literals_2():
    _test_binary_literals(5, 3, BinarySub, 2)


def test_sub_literals_3():
    _test_binary_literals(0, 0, BinarySub, 0)


def test_sub_literals_4():
    _test_binary_literals(5.5, 1.2, BinarySub, 5.5 - 1.2)


def test_sub_literals_5():
    _test_binary_literals(-3.1415, 7.0, BinarySub, -3.1415 - 7.0)


def test_mul_literals_1():
    _test_binary_literals(3, 5, BinaryMul, 15)


def test_mul_literals_2():
    _test_binary_literals(5, 3, BinaryMul, 15)


def test_mul_literals_3():
    _test_binary_literals(0, 0, BinaryMul, 0)


def test_mul_literals_4():
    _test_binary_literals(5.5, 1.2, BinaryMul, 5.5 * 1.2)


def test_mul_literals_5():
    _test_binary_literals(-3.1415, 7.0, BinaryMul, -3.1415 * 7.0)


def test_div_literals_1():
    _test_binary_literals(3, 5, BinaryDiv, 0)


def test_div_literals_2():
    _test_binary_literals(5, 3, BinaryDiv, 1)


def test_div_literals_3():
    _test_binary_literals(15, 5, BinaryDiv, 3)


def test_div_literals_4():
    _test_binary_literals(16, 6, BinaryDiv, 2)


def test_div_literals_5():
    _test_binary_literals(16., 6., BinaryDiv, 16. / 6.)


def test_div_literals_6():
    _test_binary_literals(15., 5., BinaryDiv, 3.)


def test_div_literals_7():
    _test_binary_literals(1., -1.5, BinaryDiv, 1. / -1.5)


def _test_binary_literals(a, b, op, expect):
    a_int = isinstance(a, int)
    b_int = isinstance(b, int)

    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            op(children=[
                Literal(value=a, type=NumericType(is_int=a_int)),
                Literal(value=b, type=NumericType(is_int=b_int))
            ])
        ])
    ])

    actual, expect = float(get_test_stdout(module)), float(expect)
    assert math.isclose(actual, expect, abs_tol=.01, rel_tol=.01)


def test_add_vars_1():
    _test_binary_vars(3, 5, BinaryAdd, 8)


def test_add_vars_2():
    _test_binary_vars(0, 0, BinaryAdd, 0)


def test_add_vars_3():
    _test_binary_vars(-5, 10, BinaryAdd, 5)


def test_add_vars_4():
    _test_binary_vars(5.5, 1.2, BinaryAdd, 5.5 + 1.2)


def test_add_vars_5():
    _test_binary_vars(-3.1415, 7.0, BinaryAdd, -3.1415 + 7.0)


def test_sub_vars_1():
    _test_binary_vars(3, 5, BinarySub, -2)


def test_sub_vars_2():
    _test_binary_vars(5, 3, BinarySub, 2)


def test_sub_vars_3():
    _test_binary_vars(0, 0, BinarySub, 0)


def test_sub_vars_4():
    _test_binary_vars(5.5, 1.2, BinarySub, 5.5 - 1.2)


def test_sub_vars_5():
    _test_binary_vars(-3.1415, 7.0, BinarySub, -3.1415 - 7.0)


def test_mul_vars_1():
    _test_binary_vars(3, 5, BinaryMul, 15)


def test_mul_vars_2():
    _test_binary_vars(5, 3, BinaryMul, 15)


def test_mul_vars_3():
    _test_binary_vars(0, 0, BinaryMul, 0)


def test_mul_vars_4():
    _test_binary_vars(5.5, 1.2, BinaryMul, 5.5 * 1.2)


def test_mul_vars_5():
    _test_binary_vars(-3.1415, 7.0, BinaryMul, -3.1415 * 7.0)


def test_div_vars_1():
    _test_binary_vars(3, 5, BinaryDiv, 0)


def test_div_vars_2():
    _test_binary_vars(5, 3, BinaryDiv, 1)


def test_div_vars_3():
    _test_binary_vars(15, 5, BinaryDiv, 3)


def test_div_vars_4():
    _test_binary_vars(16, 6, BinaryDiv, 2)


def test_div_vars_5():
    _test_binary_vars(16., 6., BinaryDiv, 16. / 6.)


def test_div_vars_6():
    _test_binary_vars(15., 5., BinaryDiv, 3.)


def test_div_vars_7():
    _test_binary_vars(1., -1.5, BinaryDiv, 1. / -1.5)


def _test_binary_vars(a, b, op, expect):
    a_int = isinstance(a, int)
    b_int = isinstance(b, int)

    module = Module(is_main=True, name='_main_', children=[
        DefVar('a'),
        Assign(children=[
            BareName('a'),
            Literal(value=a, type=NumericType(is_int=a_int)),
        ]),
        DefVar('b'),
        Assign(children=[
            BareName('b'),
            Literal(value=b, type=NumericType(is_int=b_int)),
        ]),
        Print(children=[
            op(children=[BareName('a'), BareName('b')])
        ])
    ])

    actual, expect = float(get_test_stdout(module)), float(expect)
    assert math.isclose(actual, expect, abs_tol=.01, rel_tol=.01)
