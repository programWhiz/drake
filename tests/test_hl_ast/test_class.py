from src.hl_ast import Module, Assign, BareName, Literal, NumericType, Invoke, Print, DefVar, FuncDefArg, FuncDef, \
    InvokeArg
from src.hl_ast.class_def import *
from .test_base import get_test_stdout


def test_empty_class():
    EmptyClass = ClassDef(name='EmptyClass', children=[])

    module = Module(
        is_main=True, name='_main_', children=[
            EmptyClass,
            Invoke(children=[ BareName("EmptyClass") ])
        ])

    result = get_test_stdout(module)
    assert result == ""


def test_class_single_field():
    TestClass = ClassDef(name='TestClass', fields=OrderedDict(
        a=NumericType(is_int=True, precision=32)
    ))

    module = Module(
        is_main=True, name='_main_', children=[
            TestClass,
            Invoke(children=[ BareName("TestClass") ])
        ])

    result = get_test_stdout(module)
    assert result == ""


def test_class_simple_assign():
    int_type = NumericType(is_int=True, precision=32)

    TestClass = ClassDef(name='TestClass_2', fields=OrderedDict(
        a=int_type
    ))

    module = Module(
        is_main=True, name='_main_', children=[
            TestClass,
            DefVar(name='test_inst'),
            Assign(children=[
                BareName('test_inst'),
                Invoke(children=[ BareName("TestClass_2") ])
            ]),
            # # test_inst.a = 123
            Assign(children=[
                GetAttr(children=[BareName("test_inst"), GetAttrField('a')]),
                Literal(type=int_type, value=123)
            ]),
            # print(test_inst.a)
            Print(children=[
                GetAttr(children=[BareName("test_inst"), GetAttrField('a')]),
            ])
        ])

    result = get_test_stdout(module)
    assert result == "123"
