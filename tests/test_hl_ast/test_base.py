import os
import subprocess
import tempfile
from pprint import pformat

from src.cpp_builder import CPPBuilder, compile_cpp_module
from src.llvm_ast import compile_module_ir
from src.llvm_utils import compile_module_llvm, create_binary_executable, llvm_shutdown


def get_test_stdout_llvm(root_node):
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


def get_test_stdout(root_node, compile_only=False):
    source_path = tempfile.mktemp(dir="/tmp", prefix="drake_test", suffix=".cpp")
    header_path = source_path.replace('.cpp', '.hpp')
    exe_path = source_path.replace('.cpp', '')

    with CPPBuilder(c=source_path, h=header_path) as builder:
        root_node.to_cpp(builder)

    print("\nCPP header file:\n", open(header_path).read())
    print("\nCPP source file:\n", open(source_path).read())

    compile_cpp_module([ source_path ], exe_path)

    if compile_only:
        return None

    output = subprocess.check_output(exe_path)
    output = output.decode('utf-8').strip()

    return output
