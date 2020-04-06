import os
import subprocess
import tempfile
from pprint import pformat
from src.cpp_builder import CPPBuilder, compile_cpp_module


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
