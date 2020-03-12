import math

from src.hl_ast import Literal, NumericType, Module, Printf, StrLiteral, CastType, Print
from tests.test_hl_ast.test_base import get_test_stdout


def test_printf_int():
    number = Literal(14, type=NumericType(is_int=True, precision=32))

    module = Module(is_main=True, name='_main_', children=[
        Printf(children=[ StrLiteral("%d"), number ])
    ])

    result = get_test_stdout(module)
    assert result == "14"


def test_printf_str():
    module = Module(is_main=True, name='_main_', children=[
        Printf(children=[ StrLiteral("Hello world 世界!") ])
    ])

    result = get_test_stdout(module)
    assert result == "Hello world 世界!"


def test_printf_float():
    number = Literal(3.1415, type=NumericType(is_int=False, precision=32))

    module = Module(is_main=True, name='_main_', children=[
        Printf(children=[
            StrLiteral("%.04f"),
            CastType('fpext', type=NumericType(is_int=False, precision=64), children=[ number ])
        ])
    ])

    result = get_test_stdout(module)
    assert result == "3.1415"


def test_printf_double():
    number = Literal(3.1415, type=NumericType(is_int=False, precision=64))

    module = Module(is_main=True, name='_main_', children=[
        Printf(children=[ StrLiteral("%.04lf"), number ])
    ])

    result = get_test_stdout(module)
    assert result == "3.1415"


def test_print_str():
    module = Module(is_main=True, name='_main_', children=[
        Print(children=[ StrLiteral("Hello world 世界!") ])
    ])

    result = get_test_stdout(module)
    assert result == "Hello world 世界!"


def test_print_int():
    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            Literal(1, type=NumericType(is_int=True, is_bool=True, precision=8)),
            Literal(8, type=NumericType(is_int=True, precision=8)),
            Literal(16, type=NumericType(is_int=True, precision=16)),
            Literal(32, type=NumericType(is_int=True, precision=32)),
            Literal(64, type=NumericType(is_int=True, precision=64)),
        ])
    ])

    result = get_test_stdout(module)
    assert result == "1 8 16 32 64"


def test_print_float():
    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            Literal(1.234, type=NumericType(is_int=False, precision=32)),
            Literal(3.141519, type=NumericType(is_int=False, precision=64)),
        ])
    ])

    result = get_test_stdout(module)
    numbers = [ float(x) for x in result.split(' ') ]
    assert math.isclose(numbers[0], 1.234)
    assert math.isclose(numbers[1], 3.141519)