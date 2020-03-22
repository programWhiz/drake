from src.exceptions import BuildException
from src.hl_ast import Module, FuncDef, Print, StrLiteral, Invoke, BareName, FuncDefArg, InvokeArg, Literal, \
    NumericType, Printf
from .test_base import get_test_stdout
import re


def test_func_no_args():
    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[], children=[
            Print(children=[StrLiteral("Hello world")])
        ]),
        Invoke(children=[ BareName('test_func') ])
    ])
    result = get_test_stdout(module)
    assert result == "Hello world"


def test_empty_func_no_args():
    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[], children=[
        ]),
        Invoke(children=[ BareName('test_func') ])
    ])
    result = get_test_stdout(module)
    assert result == ""


def test_empty_func_with_args():
    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[
            FuncDefArg("x"), FuncDefArg("y") ]),
        Invoke(children=[
            BareName('test_func'),
            InvokeArg(name=None, index=0, value=
                      Literal(32, type=NumericType(is_int=True, precision=32))),
            InvokeArg(name=None, index=0, value=
                Literal(32, type=NumericType(is_int=True, precision=32))),
        ])
    ])
    result = get_test_stdout(module)
    assert result == ""


def test_bind_kwargs():
    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func',
                func_args=[ FuncDefArg("x"), FuncDefArg("y") ],
                children=[
                    Printf(children=[StrLiteral("%d, %d\n"), BareName('x'), BareName('y')])
                ]),
        # Invoke with index of args only (name=None)
        Invoke(children=[
            BareName('test_func'),
            InvokeArg(name=None, index=0, value=
                Literal(1, type=NumericType(is_int=True, precision=32))),
            InvokeArg(name=None, index=1, value=
                Literal(2, type=NumericType(is_int=True, precision=32))),
        ]),
        # Invoke with names and indices
        Invoke(children=[
            BareName('test_func'),
            InvokeArg(name='x', index=0, value=
                Literal(3, type=NumericType(is_int=True, precision=32))),
            InvokeArg(name='y', index=1, value=
                Literal(4, type=NumericType(is_int=True, precision=32))),
        ]),
        # Invoke only with names (indices are null)
        Invoke(children=[
            BareName('test_func'),
            InvokeArg(name='y', index=None, value=
                Literal(6, type=NumericType(is_int=True, precision=32))),
            InvokeArg(name='x', index=None, value=
                Literal(5, type=NumericType(is_int=True, precision=32))),
        ]),
    ])
    result = get_test_stdout(module)
    assert result == "1, 2\n3, 4\n5, 6"


def test_call_func():
    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x')], children=[
            Printf(children=[StrLiteral("%d\n"), BareName('x')])
        ]),
        Invoke(children=[
            BareName('test_func'),
            InvokeArg(name=None, index=0, value=
                Literal(32, type=NumericType(is_int=True, precision=32)))
        ]),
        Invoke(children=[
            BareName('test_func'),
            InvokeArg(name=None, index=0, value=
                Literal(16, type=NumericType(is_int=True, precision=16)))
        ]),
        Invoke(children=[
            BareName('test_func'),
            InvokeArg(name=None, index=0, value=
                Literal(1, type=NumericType(is_int=True, is_bool=True, precision=8)))
        ]),
    ])

    result = get_test_stdout(module)
    assert result == "32\n16\n1"


def test_func_missing_arg():
    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x')]),
        Invoke(children=[ BareName('test_func') ]),
    ])

    try:
        get_test_stdout(module)
        assert False, "Expected BuildException"
    except BuildException:
        pass


def test_func_missing_kwarg():
    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x'), FuncDefArg('y')], children=[]),
        Invoke(children=[
            BareName('test_func'),
            InvokeArg(name='y', index=None, value=None)
        ]),
    ])

    try:
        get_test_stdout(module)
        assert False, "Expected BuildException"
    except BuildException:
        pass


def test_func_extra_kwarg():
    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x'), FuncDefArg('y')], children=[]),
        Invoke(children=[
            BareName('test_func'),
            InvokeArg(name='x', index=None, value=None),
            InvokeArg(name='y', index=None, value=None),
            InvokeArg(name='z', index=None, value=None)
        ]),
    ])

    try:
        get_test_stdout(module)
        assert False, "Expected BuildException"
    except BuildException:
        pass


def test_func_extra_arg():
    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x'), FuncDefArg('y')], children=[]),
        Invoke(children=[
            BareName('test_func'),
            InvokeArg(index=0, value=None),
            InvokeArg(index=1, value=None),
            InvokeArg(index=2, value=None)
        ]),
    ])

    try:
        get_test_stdout(module)
        assert False, "Expected BuildException"
    except BuildException:
        pass


def test_overload_count():
    int_value = Literal(value=123, type=NumericType(is_int=True))

    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x')], children=[
            Print(children=[StrLiteral("func1")])
        ]),
        FuncDef(name='test_func', func_args=[FuncDefArg('x'), FuncDefArg('y')], children=[
            Print(children=[StrLiteral("func2")])
        ]),
        Invoke(children=[  # test_func(x, y) => "func2"
            BareName('test_func'),
            InvokeArg(index=0, value=int_value),
            InvokeArg(index=1, value=int_value),
        ]),
        Invoke(children=[   # test_func(x) => "func1"
            BareName('test_func'),
            InvokeArg(index=0, value=int_value),
        ]),
    ])

    result = get_test_stdout(module)
    assert result == "func2\nfunc1"


def test_print_float():
    float_type = NumericType(is_int=False, is_fixed=True, precision=32)
    float_value = Literal(value=1.23, type=float_type)

    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=float_type)], children=[
            Print(children=[BareName('x')])
        ]),
        Invoke(children=[   # test_func(1.23)
            BareName('test_func'), InvokeArg(index=0, value=float_value),
        ]),
    ])

    result = get_test_stdout(module)
    assert re.match(r"1.230*", result)


def test_implicit_cast_int_arg():
    int_type = NumericType(is_int=True, is_fixed=True, precision=32)
    long_type = NumericType(is_int=True, precision=64)
    long_value = Literal(value=123, type=long_type)

    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=int_type)], children=[
            Print(children=[BareName('x')])
        ]),
        Invoke(children=[   # test_func(1.23)
            BareName('test_func'), InvokeArg(index=0, value=long_value),
        ]),
    ])

    result = get_test_stdout(module)
    assert result == "123"


def test_implicit_cast_float_arg():
    float_type = NumericType(is_int=False, is_fixed=True, precision=32)
    double_type = NumericType(is_int=False, precision=64)
    double_value = Literal(value=1.23, type=double_type)

    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=float_type)], children=[
            Print(children=[BareName('x')])
        ]),
        Invoke(children=[   # test_func(1.23)
            BareName('test_func'), InvokeArg(index=0, value=double_value),
        ]),
    ])

    result = get_test_stdout(module)
    assert result[0:4] == "1.23"


def test_overload_by_type():
    int_value = Literal(value=123, type=NumericType(is_int=True))
    float_value = Literal(value=1.23, type=NumericType(is_int=False, precision=32))
    int_type = NumericType(is_int=True, is_fixed=True)
    float_type = NumericType(is_int=False, is_fixed=True)

    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=int_type)], children=[
            Print(children=[BareName('x')])
        ]),
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=float_type)], children=[
            Print(children=[BareName('x')])
        ]),
        Invoke(children=[  # test_func(123)
            BareName('test_func'), InvokeArg(index=0, value=int_value),
        ]),
        Invoke(children=[   # test_func(1.23)
            BareName('test_func'), InvokeArg(index=0, value=float_value),
        ]),
    ])

    result = get_test_stdout(module)
    assert re.match("123\n1.230*", result)


def test_overload_by_type():
    int_value = Literal(value=123, type=NumericType(is_int=True))
    float_value = Literal(value=1.23, type=NumericType(is_int=False, precision=32))
    int_type = NumericType(is_int=True, is_fixed=True)
    float_type = NumericType(is_int=False, is_fixed=True)

    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=int_type)], children=[
            Print(children=[BareName('x')])
        ]),
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=float_type)], children=[
            Print(children=[BareName('x')])
        ]),
        Invoke(children=[  # test_func(123)
            BareName('test_func'), InvokeArg(index=0, value=int_value),
        ]),
        Invoke(children=[   # test_func(1.23)
            BareName('test_func'), InvokeArg(index=0, value=float_value),
        ]),
    ])

    result = get_test_stdout(module)
    assert re.match("123\n1.230*", result)


def test_overload_prefer_non_cast():
    """Test that a function overload will preferentially choose a function that does not require overload."""
    int8, int16, int32 = ( NumericType(precision=p) for p in (8, 16, 32) )

    module = Module(is_main=True, name='_main_', children=[
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=int32)], children=[
            Print(children=[StrLiteral(value="int32"), BareName('x')])
        ]),
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=int16)], children=[
            Print(children=[StrLiteral(value="int16"), BareName('x')])
        ]),
        # Call with int32 value, should choose first overload
        Invoke(children=[
            BareName('test_func'), InvokeArg(index=0, value=Literal(value=123, type=int32)),
        ]),
        # Call with int16 value, should choose second overload
        Invoke(children=[
            BareName('test_func'), InvokeArg(index=0, value=Literal(value=456, type=int16)),
        ]),
    ])

    result = get_test_stdout(module)
    assert result == "int32 123\nint16 456"


def test_multiple_overload_cast_fail():
    """Test that a overloading fails when casting to multiple types could work."""

    int8, int16, int32 = ( NumericType(precision=p) for p in (8, 16, 32) )

    module = Module(is_main=True, name='_main_', children=[
        # def test_func(int32 x)
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=int32)], children=[
            Print(children=[StrLiteral(value="int32"), BareName('x')])
        ]),
        # def test_func(int16 x)
        FuncDef(name='test_func', func_args=[FuncDefArg('x', dtype=int16)], children=[
            Print(children=[StrLiteral(value="int16"), BareName('x')])
        ]),
        # Call with int8 value, could choose either func impl
        Invoke(children=[
            BareName('test_func'), InvokeArg(index=0, value=Literal(value=123, type=int8)),
        ]),
    ])

    try:
        get_test_stdout(module)
        assert False, "Expected ambiguous overload to fail."
    except:
        pass


def test_call_default_value():
    int32 = NumericType()

    module = Module(is_main=True, name='_main_', children=[
        # def test_func(int32 x = 123)
        FuncDef(name='test_func', func_args=[
            FuncDefArg('x', dtype=int32, default_val=Literal(value=123, type=int32))
        ], children=[
            Print(children=[StrLiteral(value="int32"), BareName('x')])
        ]),
        Invoke(children=[ BareName('test_func') ])
    ])

    assert get_test_stdout(module) == 'int32 123'


def test_call_multi_default_values():
    int32 = NumericType()

    module = Module(is_main=True, name='_main_', children=[
        # def test_func(int32 x = 123)
        FuncDef(name='test_func', func_args=[
            FuncDefArg('x', dtype=int32, default_val=Literal(value=123, type=int32)),
            FuncDefArg('y', dtype=int32, default_val=Literal(value=456, type=int32)),
            FuncDefArg('z', dtype=int32, default_val=Literal(value=789, type=int32)),
        ], children=[
            Print(children=[ BareName('x'), BareName('y'), BareName('z'), ])
        ]),
        Invoke(children=[ BareName('test_func') ]),
        # Zero out one arg at a time by name
        Invoke(children=[BareName('test_func'), InvokeArg(name='x', value=Literal(value=0, type=int32))]),
        Invoke(children=[BareName('test_func'), InvokeArg(name='y', value=Literal(value=0, type=int32))]),
        Invoke(children=[BareName('test_func'), InvokeArg(name='z', value=Literal(value=0, type=int32))]),
        # Zero out args by position
        Invoke(children=[BareName('test_func'), InvokeArg(index=0, value=Literal(value=0, type=int32))]),
        Invoke(children=[BareName('test_func'),
                         InvokeArg(index=0, value=Literal(value=0, type=int32)),
                         InvokeArg(index=1, value=Literal(value=0, type=int32)) ]),
        Invoke(children=[BareName('test_func'),
                         InvokeArg(index=0, value=Literal(value=0, type=int32)),
                         InvokeArg(index=1, value=Literal(value=0, type=int32)),
                         InvokeArg(index=2, value=Literal(value=0, type=int32)) ]),
    ])

    results = get_test_stdout(module).split('\n')
    # Pass no args, all use default values
    assert results[0] == '123 456 789'
    # Zero args by name
    assert results[1] == '0 456 789'
    assert results[2] == '123 0 789'
    assert results[3] == '123 456 0'
    # Zero args by position
    assert results[4] == '0 456 789'
    assert results[5] == '0 0 789'
    assert results[6] == '0 0 0'
