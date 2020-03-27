import math

from .test_base import get_test_stdout
from src.hl_ast import *


def test_add_literals():
    _test_binary_literals(3, 5, BinaryAdd, 8)
    _test_binary_literals(0, 0, BinaryAdd, 0)
    _test_binary_literals(-5, 10, BinaryAdd, 5)
    _test_binary_literals(5.5, 1.2, BinaryAdd, 5.5 + 1.2)
    _test_binary_literals(-3.1415, 7.0, BinaryAdd, -3.1415 + 7.0)


def test_sub_literals():
    _test_binary_literals(3, 5, BinarySub, -2)
    _test_binary_literals(5, 3, BinarySub, 2)
    _test_binary_literals(0, 0, BinarySub, 0)
    _test_binary_literals(5.5, 1.2, BinarySub, 5.5 - 1.2)
    _test_binary_literals(-3.1415, 7.0, BinarySub, -3.1415 - 7.0)


def test_mul_literals():
    _test_binary_literals(3, 5, BinaryMul, 15)
    _test_binary_literals(5, 3, BinaryMul, 15)
    _test_binary_literals(0, 0, BinaryMul, 0)
    _test_binary_literals(5.5, 1.2, BinaryMul, 5.5 * 1.2)
    _test_binary_literals(-3.1415, 7.0, BinaryMul, -3.1415 * 7.0)


def test_div_literals():
    _test_binary_literals(3, 5, BinaryDiv, 0)
    _test_binary_literals(5, 3, BinaryDiv, 1)
    _test_binary_literals(15, 5, BinaryDiv, 3)
    _test_binary_literals(16, 6, BinaryDiv, 2)
    _test_binary_literals(16., 6., BinaryDiv, 16. / 6.)
    _test_binary_literals(15., 5., BinaryDiv, 3.)
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


def test_add_vars():
    _test_binary_vars(3, 5, BinaryAdd, 8)
    _test_binary_vars(0, 0, BinaryAdd, 0)
    _test_binary_vars(-5, 10, BinaryAdd, 5)
    _test_binary_vars(5.5, 1.2, BinaryAdd, 5.5 + 1.2)
    _test_binary_vars(-3.1415, 7.0, BinaryAdd, -3.1415 + 7.0)


def test_sub_vars():
    _test_binary_vars(3, 5, BinarySub, -2)
    _test_binary_vars(5, 3, BinarySub, 2)
    _test_binary_vars(0, 0, BinarySub, 0)
    _test_binary_vars(5.5, 1.2, BinarySub, 5.5 - 1.2)
    _test_binary_vars(-3.1415, 7.0, BinarySub, -3.1415 - 7.0)


def test_mul_vars():
    _test_binary_vars(3, 5, BinaryMul, 15)
    _test_binary_vars(5, 3, BinaryMul, 15)
    _test_binary_vars(0, 0, BinaryMul, 0)
    _test_binary_vars(5.5, 1.2, BinaryMul, 5.5 * 1.2)
    _test_binary_vars(-3.1415, 7.0, BinaryMul, -3.1415 * 7.0)


def test_div_vars():
    _test_binary_vars(3, 5, BinaryDiv, 0)
    _test_binary_vars(5, 3, BinaryDiv, 1)
    _test_binary_vars(15, 5, BinaryDiv, 3)
    _test_binary_vars(16, 6, BinaryDiv, 2)
    _test_binary_vars(16., 6., BinaryDiv, 16. / 6.)
    _test_binary_vars(15., 5., BinaryDiv, 3.)
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
            op(children=[ BareName('a'), BareName('b') ])
        ])
    ])

    actual, expect = float(get_test_stdout(module)), float(expect)
    assert math.isclose(actual, expect, abs_tol=.01, rel_tol=.01)
