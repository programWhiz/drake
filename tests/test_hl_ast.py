import subprocess
import tempfile
import os
from src.hl_ast import *
from src.llvm_ast import compile_module_ir
from src.llvm_utils import compile_module_llvm, create_binary_executable, run_cli_cmd


def get_test_stdout(module_ast):
    obj_file, exe_file = None, None
    module_path = tempfile.mktemp(dir="/tmp", prefix="drake_test_module", suffix=".ll")

    try:
        ll_ast = compile_hl_ast(module_ast, is_main=True)
        print("\nLLVM AST:\n", ll_ast)

        ll_module = compile_module_ir(ll_ast)
        print("\nLLVM code:\n", str(ll_module))

        obj_file = compile_module_llvm(module_path, ll_module)
        exe_path = tempfile.mktemp(dir='/tmp', prefix='drake_test')
        create_binary_executable(exe_path, [ obj_file ])
        output = subprocess.check_output(exe_path)
        return output.decode('utf-8').strip()
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
