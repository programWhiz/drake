import os
import subprocess
import tempfile
from pprint import pformat

from src.llvm_ast import compile_module_ir
from src.llvm_utils import compile_module_llvm, create_binary_executable, llvm_shutdown


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
        llvm_shutdown()

    return output