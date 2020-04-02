from src.hl_ast import *
from .test_base import get_test_stdout


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


def test_assign_udefined_var():
    module = Module(is_main=True, name='_main_', children=[
        Assign(children=[
            BareName('x'),   # x is undefined here (no DefVar statement)
            Literal(1234, type=NumericType(is_int=True, precision=32))
        ])
    ])

    try:
        get_test_stdout(module)
        assert False, 'Expected assign to undefined var to fail.'
    except UndefinedVariableError as e:
        pass


def test_assign_fixed_type():
    module = Module(is_main=True, name='_main_', children=[
        # x can only be type "int"
        DefVar('x', fixed_type=True, type=NumericType(is_int=True)),
        # Try to assign type "int", should pass
        Assign(children=[
            BareName('x'),
            Literal(1234, type=NumericType(is_int=True)),
        ]),
        Print(children=[ BareName('x') ]),
    ])

    assert get_test_stdout(module) == '1234'


def test_assign_fixed_type_error():
    module = Module(is_main=True, name='_main_', children=[
        # x can only be type "int"
        DefVar('x', fixed_type=True, type=NumericType(is_int=True)),
        # Try to assign type "float", should fail
        Assign(children=[
            BareName('x'),
            Literal(3.1415, type=NumericType(is_int=False, precision=32)),
        ]),
        Print(children=[ BareName('x') ]),
    ])

    try:
        get_test_stdout(module)
        assert False, 'Expected InvalidTypeError'
    except InvalidTypeError:
        pass


def test_assign_fixed_type_cast():
    module = Module(is_main=True, name='_main_', children=[
        # x can only be type int64
        DefVar('x', fixed_type=True, type=NumericType(is_int=True, precision=64)),
        # Try to assign type int32, should cast
        Assign(children=[
            BareName('x'),
            Literal(1234, type=NumericType(is_int=True, precision=32)),
        ]),
        Print(children=[ BareName('x') ]),
    ])

    assert get_test_stdout(module) == '1234'
