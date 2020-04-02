from src.hl_ast import *
from .test_base import get_test_stdout


def test_loop():
    int32 = NumericType()

    module = Module(
        is_main=True, name='_main_', children=[
            DefVar('x'),
            Assign(children=[
                BareName('x'),
                Literal(value=0, type=int32)
            ]),
            Loop(children=[
                LessThan(children=[
                    BareName('x'), Literal(value=3, type=int32)
                ]),
                InstrList(children=[
                    Print(children=[ BareName('x') ]),
                    Assign(children=[
                        BareName('x'),
                        BinaryAdd(children=[
                            BareName('x'),
                            Literal(value=1, type=int32)
                        ])
                    ])
                ])
            ])
        ])

    result = get_test_stdout(module)
    assert result == "0\n1\n2"
