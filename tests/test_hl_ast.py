import subprocess
import tempfile
import os
from pprint import pformat

from src.hl_ast import *
from src.llvm_ast import compile_module_ir
from src.llvm_utils import compile_module_llvm, create_binary_executable
import pytest


def get_test_stdout(root_node):
    obj_file, exe_file = None, None
    module_path = tempfile.mktemp(dir="/tmp", prefix="drake_test_module", suffix=".ll")

    try:
        ll_ast = root_node.to_ll_ast()
        print("\nLLVM AST:\n", pformat(ll_ast))

        ll_module = compile_module_ir(ll_ast)
        print("\nLLVM code:\n", str(ll_module))

        obj_file = compile_module_llvm(module_path, ll_module)
        exe_path = tempfile.mktemp(dir='/tmp', prefix='drake_test')
        create_binary_executable(exe_path, [ obj_file ])
        output = subprocess.check_output(exe_path)
        output = output.decode('utf-8').strip()
    finally:
        if obj_file:
            os.remove(obj_file)
        if exe_file:
            os.remove(obj_file)

    return output


def test_node_replace_empty():
    n1, n2 = Node(), Node()
    n3 = Node(children=[ n1, n2 ])
    n3.replace_child(n2, [])
    assert n3.children == [ n1 ]


def test_node_replace_single():
    n1, n2 = Node(), Node()
    n3 = Node(children=[ n1, n2 ])
    n4 = Node()
    n3.replace_child(n2, [ n4 ])
    assert n3.children == [ n1, n4 ]


def test_node_replace_multi():
    n1, n2, n3, n4 = Node(), Node(), Node(), Node()
    n5 = Node(children=[ n1, n2 ])
    n5.replace_child(n2, [ n3, n4 ])
    assert n5.children == [ n1, n3, n4 ]
    n5.replace_child(n1, [ n3, n2 ])
    assert n5.children == [ n3, n2, n3, n4 ]


def test_print_int():
    number = Literal(14, type=NumericType(is_int=True, precision=32))

    module = Module(is_main=True, name='_main_', children=[
        Printf(children=[ StrLiteral("%d"), number ])
    ])

    result = get_test_stdout(module)
    assert result == "14"


def test_print_str():
    module = Module(is_main=True, name='_main_', children=[
        Printf(children=[ StrLiteral("Hello world 世界!") ])
    ])

    result = get_test_stdout(module)
    assert result == "Hello world 世界!"


def test_print_float():
    number = Literal(3.1415, type=NumericType(is_int=False, precision=32))

    module = Module(is_main=True, name='_main_', children=[
        Printf(children=[
            StrLiteral("%.04f"),
            CastType('fpext', type=NumericType(is_int=False, precision=64), children=[ number ])
        ])
    ])

    result = get_test_stdout(module)
    assert result == "3.1415"


def test_print_double():
    number = Literal(3.1415, type=NumericType(is_int=False, precision=64))

    module = Module(is_main=True, name='_main_', children=[
        Printf(children=[ StrLiteral("%.04lf"), number ])
    ])

    result = get_test_stdout(module)
    assert result == "3.1415"


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


# def test_simple_function():
#     int_val = Literal(14, type=NumericType(is_int=True, precision=32))
#     func_tpl = FuncTemplate(
#         func_args=[],
#         children=[
#             ReturnStmt(children=[ int_val ])
#         ]
#     )


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
