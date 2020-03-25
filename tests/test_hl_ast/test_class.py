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
    int32 = NumericType(is_int=True, precision=32)

    TestClass = ClassDef(name='TestClass', fields=OrderedDict(
        a=ClassField(name='a', type=int32)
    ))

    module = Module(
        is_main=True, name='_main_', children=[
            TestClass,
            Invoke(children=[
                BareName("TestClass"),
                InvokeArg(index=0, value=Literal(value=123, type=int32))
            ])
        ])

    result = get_test_stdout(module)
    assert result == ""


def test_class_simple_assign():
    int_type = NumericType(is_int=True, precision=32)

    TestClass = ClassDef(name='TestClass_2', fields=OrderedDict(
        a=ClassField(name='a', type=int_type, default_value=Literal(value=0, type=int_type))
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


def test_class_func_param():
    int_type = NumericType(is_int=True, precision=32)

    TestClass = ClassDef(name='TestClass_3', fields=OrderedDict(
        a=ClassField(name='a', type=int_type, default_value=Literal(value=0, type=int_type))
    ))

    module = Module(
        is_main=True, name='_main_', children=[
            TestClass,
            DefVar(name='test_inst'),
            # test_inst = TestClass()
            Assign(children=[
                BareName('test_inst'),
                Invoke(children=[ BareName("TestClass_3") ])
            ]),
            # test_inst.a = 123
            Assign(children=[
                GetAttr(children=[BareName("test_inst"), GetAttrField('a')]),
                Literal(type=int_type, value=123)
            ]),
            # fn test_func(x): print(x.a);
            FuncDef(name='test_func', func_args=[ FuncDefArg('x'), ], children=[
                # print(x.a) => 123
                Print(children=[
                    GetAttr(children=[ BareName('x'), GetAttrField('a') ])
                ])
            ]),
            Invoke(children=[
                BareName('test_func'), InvokeArg(index=0, value=BareName('test_inst')),
            ]),
        ])

    result = get_test_stdout(module)
    assert result == "123"


def test_class_default_value():
    int_type = NumericType(is_int=True, precision=32)

    TestClass = ClassDef(name='TestClass_4', fields=OrderedDict(
        a=ClassField(name='a', default_value=Literal(value=123, type=int_type))
    ))

    module = Module(
        is_main=True, name='_main_', children=[
            TestClass,
            DefVar(name='test_inst'),
            Assign(children=[
                BareName('test_inst'),
                Invoke(children=[ BareName("TestClass_4") ])
            ]),
            # print(test_inst.a)
            Print(children=[
                GetAttr(children=[BareName("test_inst"), GetAttrField('a')]),
            ])
        ])

    module.build()
    result = get_test_stdout(module)
    assert result == "123"
