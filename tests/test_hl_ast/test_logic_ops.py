from .test_base import get_test_stdout
from src.hl_ast import *


def test_and():
    T = Literal(value=1, type=BoolType())
    F = Literal(value=0, type=BoolType())

    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            LogicalAnd(children=[F, F]),
            LogicalAnd(children=[F, T]),
            LogicalAnd(children=[T, F]),
            LogicalAnd(children=[T, T]),
        ])
    ])

    assert get_test_stdout(module) == '0 0 0 1'


def test_or():
    T = Literal(value=1, type=BoolType())
    F = Literal(value=0, type=BoolType())

    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            LogicalOr(children=[F, F]),
            LogicalOr(children=[F, T]),
            LogicalOr(children=[T, F]),
            LogicalOr(children=[T, T]),
        ])
    ])

    assert get_test_stdout(module) == '0 1 1 1'


def test_xor():
    T = Literal(value=1, type=BoolType())
    F = Literal(value=0, type=BoolType())

    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            LogicalXor(children=[F, F]),
            LogicalXor(children=[F, T]),
            LogicalXor(children=[T, F]),
            LogicalXor(children=[T, T]),
        ])
    ])

    assert get_test_stdout(module) == '0 1 1 0'


def test_not():
    T = Literal(value=1, type=BoolType())
    F = Literal(value=0, type=BoolType())

    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            LogicalNot(children=[F]),
            LogicalNot(children=[T]),
        ])
    ])

    assert get_test_stdout(module) == '1 0'
