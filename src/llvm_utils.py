import logging
import os
import subprocess
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

    ret = subprocess.call(llc_cmd, stdout=PIPE, stderr=PIPE)
    assert ret == 0, f"Failed to build object code from '{module_path}'!"

    return obj_file_path


def create_binary_executable(outpath:str, module_list:List[str]):
    ret = subprocess.call([ 'g++', *module_list, '-o', outpath ], stdout=PIPE, stderr=PIPE)
    assert ret == 0, "Failed to compile modules with g++."
