import subprocess
import tempfile
from src.compile import compile_string, compile_file
from src.cpp_builder import CPPBuilder, compile_cpp_module


def test_compile_str(source_code:str, compile_only=False):
    outpath = '/tmp/drake_test.dk'
    with open(outpath, 'wt') as fptr:
        fptr.write(source_code)
        fptr.write('\n')

    test_compile_file(outpath, compile_only)


def test_compile_file(file_path:str, compile_only=False):
    ast = compile_file(file_path)

    source_path = file_path.replace('.dk', '.cpp')
    header_path = file_path.replace('.dk', '.h')
    exe_path = file_path.replace('.dk', '')

    print("\nCPP header file:\n", open(header_path).read())
    print("\nCPP source file:\n", open(source_path).read())

    compile_cpp_module([ source_path ], exe_path)

    if compile_only:
        return None

    output = subprocess.check_output(exe_path)
    output = output.decode('utf-8').strip()

    return output

