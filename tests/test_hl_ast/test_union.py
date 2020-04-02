from src.hl_ast import *
from .test_base import get_test_stdout


def test_assign_udefined_var():
    i32, f32 = NumericType(), NumericType(is_int=False)

    module = Module(is_main=True, name='_main_', children=[
        DefVar('x', type=UnionType(types=[ i32, f32 ])),
        Print(children=[ BareName('x') ])
    ])

    get_test_stdout(module)
