from .test_base import get_test_stdout
from src.hl_ast import Module, Print, GreaterThan, LessThan, Literal, NumericType, EqualTo


def test_gt_ints():
    int32 = NumericType()
    literal_5 = Literal(value=5, type=int32)
    literal_3 = Literal(value=3, type=int32)

    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            GreaterThan(children=[ literal_5, literal_3 ]),
            GreaterThan(children=[ literal_3, literal_5 ]),
        ])
    ])

    assert get_test_stdout(module) == '1 0'


def test_lt_ints():
    int32 = NumericType()
    literal_5 = Literal(value=5, type=int32)
    literal_3 = Literal(value=3, type=int32)

    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            LessThan(children=[ literal_5, literal_3 ]),
            LessThan(children=[ literal_3, literal_5 ]),
        ])
    ])

    assert get_test_stdout(module) == '0 1'


def test_gt_floats():
    float32 = NumericType(is_int=False, precision=32)
    literal_5 = Literal(value=5.4, type=float32)
    literal_3 = Literal(value=3.5, type=float32)

    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            GreaterThan(children=[ literal_5, literal_3 ]),
            GreaterThan(children=[ literal_3, literal_5 ]),
        ])
    ])

    assert get_test_stdout(module) == '1 0'


def test_eq_floats():
    float32 = NumericType(is_int=False, precision=32)
    literal_5 = Literal(value=5.4, type=float32)
    literal_3 = Literal(value=3.5, type=float32)

    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            EqualTo(children=[ literal_5, literal_3 ]),
            EqualTo(children=[ literal_3, literal_5 ]),
            EqualTo(children=[literal_5, literal_5]),
            EqualTo(children=[literal_3, literal_3]),
        ])
    ])

    assert get_test_stdout(module) == '0 0 1 1'


def test_type_cast():
    float32 = NumericType(is_int=False, precision=32)
    int32, int8 = NumericType(), NumericType(precision=8)
    literal_5 = Literal(value=5, type=int32)
    literal_3 = Literal(value=3.5, type=float32)
    literal_2 = Literal(value=2, type=int8)

    module = Module(is_main=True, name='_main_', children=[
        Print(children=[
            GreaterThan(children=[ literal_5, literal_3 ]),
            GreaterThan(children=[ literal_3, literal_5 ]),
            GreaterThan(children=[ literal_2, literal_3 ]),
            GreaterThan(children=[ literal_3, literal_2 ]),
            LessThan(children=[literal_5, literal_3]),
            LessThan(children=[literal_3, literal_5]),
            LessThan(children=[literal_5, literal_2]),
            LessThan(children=[literal_2, literal_5]),
        ])
    ])

    assert get_test_stdout(module) == '1 0 0 1 0 1 0 1'
