import subprocess
import tempfile
import os
from src.hl_ast import *
from src.llvm_ast import compile_module_ir
from src.llvm_utils import compile_module_llvm, create_binary_executable, run_cli_cmd
import pytest


def get_test_stdout(root_node):
    obj_file, exe_file = None, None
    module_path = tempfile.mktemp(dir="/tmp", prefix="drake_test_module", suffix=".ll")

    try:
        ll_ast = root_node.to_ll_ast()
        print("\nLLVM AST:\n", ll_ast)

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


def test_print():
    module = {
        "name": "_main_",
        "instrs": [
            { "op": "printf", "args": [ make_str("Hello world 世界!") ] }
        ]
    }

    result = get_test_stdout(module)
    assert result == "Hello world 世界!"


def test_bind_on_assign():
    module = {
        "name": "test_module",
        "instrs": [
            { "op": "declare_local", "name": "x", "type": None, "id": next_id() },
            {
                "op": "assign",
                "left": { "op": "get_var", "name": "x" },
                "right": make_int(42)
            },
            {
                "op": "printf",
                "args": [
                    make_str("%d"),
                    { "op": "as_arg", "ref": { "op": "get_var", "name": "x" } }
                ]
            }
        ]
    }

    result = get_test_stdout(module)
    assert result == 42


def test_print_int():
    module = {
        "name": "_main_",
        "instrs": [
            { "op": "printf", "args": [ make_str('%d'), make_int(42) ] }
        ]
    }

    result = get_test_stdout(module)
    assert result == "42"


def test_var_bind_fail_return():
    x = { "op": "declare_local", "name": "x", "type": None, "id": next_id() }

    test_func = {
        "name": "test_func",
        "id": next_id(),
        "instrs": [
            x,
            # Can't return x, unknown type
            { "op": "return", "value": { "op": "local_var", "id": x['id'] } }
        ]
    }

    compile_hl_ast({
        'name': 'test_module',
        'funcs': [ test_func ],
        'instrs': [
            { "op": "call", "func": test_func, "args": [] }
        ]
    })


def test_var_bind_fail_add():
    x = { "op": "declare_local", "name": "x", "type": None, "id": next_id() }
    y = { "op": "declare_local", "name": "y", "type": None, "id": next_id() }

    # var x, y
    # x + y
    module = {
        "name": "test_module",
        "instrs": [
            x, y,
            { "op": "add",
              "left": { "op": "get_var", "name": "x" },
              "right": { "op": "get_var", "name": "y" } }
        ]
    }

    compile_hl_ast(module)


def test_var_bind_add():
    x = { "op": "var", "name": "x", "type": make_int(3), "id": next_id() }
    y = { "op": "var", "name": "y", "type": make_int(5), "id": next_id() }
    z = { "op": "var", "name": "z", "type": None, "id": next_id() }

    # var x, y
    # x + y
    module = {
        "name": "test_module",
        "instrs": [
            x, y, z,
            {
              "op": "assign",
              "left": z,
              "right": { "op": "add", "left": x, "right": y }
            },
            { "op": "printf", "args": [ make_str("%d"), z ] }
        ]
    }

    result = get_test_stdout(module)
    assert result == 8


def test_duplicate_var_name():
    Warnings.duplicate_var.level = Warnings.ERROR

    x = { "op": "declare_local", "name": "x", "type": make_int(3), "id": next_id() }
    x2 = { "op": "declare_local", "name": "x", "type": make_int(5), "id": next_id() }

    # var x = 3
    # var x = 5
    module = {
        "name": "test_module",
        "instrs": [ x, x2 ]
    }

    try:
        get_test_stdout(module)
        assert False, 'Expected duplicate variable to throw'
    except BuildException:
        pass


def test_duplicate_var_id():
    Warnings.duplicate_var.level = Warnings.ERROR

    x = { "op": "declare_local", "name": "x", "type": make_int(3), "id": next_id() }
    y = { "op": "declare_local", "name": "y", "type": make_int(5), "id": next_id() }

    # This is bad
    y['id'] = x['id']

    # var x = 3
    # var x = 5
    module = {
        "name": "test_module",
        "instrs": [ x, y ]
    }

    try:
        get_test_stdout(module)
        assert False, 'Expected duplicate variable id to throw'
    except BuildException:
        pass


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


def test_printf():
    number = Literal(14, type=NumericType(is_int=True, precision=32))

    module = Module(is_main=True, name='_main_', children=[
        Printf(children=[ StrLiteral("%d"), number ])
    ])

    result = get_test_stdout(module)
    assert result == "14"
