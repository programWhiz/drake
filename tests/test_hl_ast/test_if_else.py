from .test_base import get_test_stdout
from src.hl_ast import *


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


def test_if_else_same_types():
    int32 = NumericType()

    module = Module(is_main=True, name='_main_', children=[
        DefVar('x'),
        # x = 0 ? 5 : 3
        IfStmt(children=[
            Literal(1, type=BoolType()),
            InstrList(children=[
                Assign(children=[BareName('x'), Literal(value=5, type=int32)]),
            ]),
            InstrList(children=[
                Assign(children=[BareName('x'), Literal(value=3, type=int32)]),
            ])
        ]),
        Print(children=[BareName('x')]),
        # x = 1 ? 5 : 3
        IfStmt(children=[
            Literal(0, type=BoolType()),
            InstrList(children=[
                Assign(children=[BareName('x'), Literal(value=5, type=int32)]),
            ]),
            InstrList(children=[
                Assign(children=[BareName('x'), Literal(value=3, type=int32)]),
            ])
        ]),
        Print(children=[BareName('x')]),
    ])

    assert get_test_stdout(module) == '5\n3'


def test_if_else_diff_types():
    int32, float32 = NumericType(), NumericType(is_int=False)

    module = Module(is_main=True, name='_main_', children=[
        DefVar('x'),
        # x = 0 ? 5 : 3.1415
        IfStmt(children=[
            Literal(0, type=BoolType()),
            InstrList(children=[
                Assign(children=[BareName('x'), Literal(value=5, type=int32)]),
            ]),
            InstrList(children=[
                Assign(children=[BareName('x'), Literal(value=3.1415, type=float32)]),
            ])
        ]),
        Print(children=[BareName('x')]),
        # # x = 1 ? 5 : 3.1415
        # IfStmt(children=[
        #     Literal(0, type=BoolType()),
        #     InstrList(children=[
        #         Assign(children=[BareName('x'), Literal(value=5, type=int32)]),
        #     ]),
        #     InstrList(children=[
        #         Assign(children=[BareName('x'), Literal(value=3.1415, type=float32)]),
        #     ])
        # ]),
        # Print(children=[BareName('x')]),
    ])

    out = get_test_stdout(module).split('\n')
    assert int(out[0]) == 5
    assert int(out[1]) == 3.1415
