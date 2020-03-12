from src.exceptions import BuildException
from src.hl_ast import Module, FuncDef, Print, StrLiteral, Invoke, BareName, FuncDefArg, InvokeArg, Literal, \
    NumericType, Printf
from tests.test_hl_ast.test_base import get_test_stdout


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