from src.hl_ast import Literal, NumericType, DefVar, Assign, BareName, Module, Printf, StrLiteral
from tests.test_hl_ast.test_base import get_test_stdout


def test_assign():
    number = Literal(14, type=NumericType(is_int=True, precision=32))
    decl_x = DefVar(name='x')
    ass_x = Assign(children=[ BareName('x'), number ])

    module = Module(is_main=True, name='_main_', children=[
        decl_x, ass_x,
        Printf(children=[ StrLiteral("%d"), BareName('x') ])
    ])

    result = get_test_stdout(module)
    assert result == "14"


def test_assign_change_type():
    int_val = Literal(14, type=NumericType(is_int=True, precision=32))
    float_val = Literal(3.1415, type=NumericType(is_int=False, precision=64))

    decl_x = DefVar(name='x')
    ass_x = Assign(children=[ BareName('x'), int_val ])
    ass_x_float = Assign(children=[ BareName('x'), float_val ])

    module = Module(is_main=True, name='_main_', children=[
        decl_x,
        ass_x,
        Printf(children=[ StrLiteral("%d\n"), BareName('x') ]),
        ass_x_float,
        Printf(children=[ StrLiteral("%.04f\n"), BareName('x') ]),
    ])

    result = get_test_stdout(module)
    assert result == "14\n3.1415"