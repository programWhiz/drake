from src.hl_ast import Module, FuncDef, Print, StrLiteral, Invoke, BareName, FuncDefArg, InvokeArg, Literal, NumericType
from .test_base import get_test_stdout


def test_call_func_ptr():
    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[ FuncDefArg('x') ], children=[
            Print(children=[StrLiteral(value="int32"), BareName('x')])
        ]),
        Invoke(children=[ BareName('test_func2') ])
    ])

    assert get_test_stdout(module) == 'int32 123'
