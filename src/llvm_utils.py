from datetime import datetime
import logging
import os
import subprocess
import sys
from subprocess import PIPE
from typing import List

import llvmlite.ir as ll
import llvmlite.binding as llvm

llvm_root = os.getenv("LLVM_HOME", "/usr/local/opt/llvm/")
llc_exe_path = None
llvm_target = None
llvm_target_machine = None


def init_llvm_compiler():
    global llc_exe_path, llvm_target, llvm_target_machine

    if all((llc_exe_path, llvm_target, llvm_target_machine)):
        return

    path = os.path.join(llvm_root, 'bin', 'llc')
    if not (os.path.exists(path) and os.access(path, os.X_OK)):
       raise FileNotFoundError(f"Could not find 'llc' program in LLVM_HOME ({llvm_root})")

    llc_exe_path = path

    # These LLVM system settings are shared between all modules
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    llvm_target = llvm.Target.from_default_triple()
    llvm_target_machine = llvm_target.create_target_machine()


def build_main_method(module, module_init_func:List[ll.Function]) -> ll.Function:
    argc = ll.IntType(32) # int argc
    argv = ll.PointerType(ll.PointerType(ll.IntType(8)))  # char** argv
    # int main( int argc, char** argv )
    ftype = ll.FunctionType(ll.IntType(32), [ argc, argv ])
    main_func = ll.Function(module, ftype, 'main')

    bb = ll.IRBuilder()
    bb.position_at_end(main_func.append_basic_block())
    bb.call(module_init_func, [])
    bb.ret(ll.Constant(ll.IntType(32), 0))

    return main_func


def compile_module_llvm(module_path:str, module:ll.Module) -> str:
    if llvm_target is None:
        init_llvm_compiler()

    module.triple = llvm_target.triple
    module.data_layout = llvm_target_machine.target_data

    module_path_base = os.path.splitext(module_path)[0]
    ll_file_path = module_path_base + '.ll'
    obj_file_path = module_path_base + '.o'

    logging.debug(f"Compiling LLVM code from module '%s' to '%s'", module_path, ll_file_path)
    with open(ll_file_path, 'wt') as fptr:
        fptr.write(str(module))

    logging.debug(f"Compiling object code from module '%s' to '%s'", module_path, obj_file_path)
    llc_cmd = [llc_exe_path, '-filetype=obj', '-o', obj_file_path, ll_file_path]
    ret = run_cli_cmd(llc_cmd)
    assert ret == 0, f"Failed to build object code from '{module_path}'!"

    return obj_file_path


def run_cli_cmd(cmd):
    # cmd = ' '.join(shlex.quote(arg) for arg in cmd)
    proc = subprocess.run(cmd, stdout=PIPE, stderr=PIPE)
    print(proc.stdout.decode('utf-8'), file=sys.stdout)
    print(proc.stderr.decode('utf-8'), file=sys.stderr)
    return proc.returncode


def create_binary_executable(outpath:str, module_list:List[str], run_exe=False):
    ret = run_cli_cmd([ 'g++', *module_list, '-o', outpath ])
    assert ret == 0, "Failed to compile modules with g++."

    if run_exe:
        logging.info("Running executable: %s", outpath)
        start_time = datetime.utcnow()

        return_code = run_cli_cmd(outpath)

        end_time = datetime.utcnow()
        logging.info("Executable %s exited with code: %d", outpath, return_code)
        logging.info("Executable %s duration: %s", outpath, end_time - start_time)
