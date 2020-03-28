from .test_base import get_test_stdout
from src.hl_ast import Module, IfStmt, InstrList, Print, BareName, Assign, DefVar, GreaterThan, Literal, NumericType


def test_if_else():
    int32 = NumericType()

    module = Module(is_main=True, name='_main_', children=[
        DefVar('x'),
        Assign(children=[ BareName('x'), Literal(value=5, type=int32)]),
        DefVar('y'),
        Assign(children=[ BareName('y'), Literal(value=3, type=int32)]),
        IfStmt(children=[
            GreaterThan(children=[ BareName('x'), BareName('y') ]),
            InstrList(children=[ Print(children=[ BareName('x') ])]),
            InstrList(children=[ Print(children=[ BareName('y') ]) ])
        ]),
        IfStmt(children=[
            GreaterThan(children=[BareName('y'), BareName('x')]),
            InstrList(children=[Print(children=[ BareName('x') ])]),
            InstrList(children=[Print(children=[ BareName('y') ])])
        ])
    ])

    assert get_test_stdout(module) == '5\n3'
