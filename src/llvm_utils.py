from ctypes import CFUNCTYPE
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


def llvm_shutdown():
    llvm.shutdown()
    global llc_exe_path, llvm_target, llvm_target_machine
    llc_exe_path = None
    llvm_target = None
    llvm_target_machine = None


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

    compile_to_object_code(module_path, ll_file_path, obj_file_path)
    return obj_file_path


def compile_to_object_code(module_path:str, ll_file_path:str, obj_file_path:str):
    init_llvm_compiler()
    logging.debug(f"Compiling object code from module '%s' to '%s'", module_path, obj_file_path)
    llc_cmd = [llc_exe_path, '-filetype=obj', '-o', obj_file_path, ll_file_path]
    ret = run_cli_cmd(llc_cmd)
    assert ret == 0, f"Failed to build object code from '{module_path}'!"


def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    init_llvm_compiler()
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def run_ir_code(module:ll.Module, func_name:str, cfunctype:CFUNCTYPE, func_args:list):
    init_llvm_compiler()

    module.triple = llvm_target.triple
    module.data_layout = llvm_target_machine.target_data
    return run_llvm_code(str(module), func_name, cfunctype, func_args)


def run_llvm_code(code:str, func_name:str, cfunctype:CFUNCTYPE, func_args:list):
    mod = llvm.parse_assembly(code)
    mod.verify()

    engine = create_execution_engine()
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()

    func_ptr = engine.get_function_address(func_name)
    cfunc = cfunctype(func_ptr)
    return cfunc(*func_args)


def run_cli_cmd(cmd):
    proc = subprocess.run(cmd, stdout=PIPE, stderr=PIPE)
    print(proc.stdout.decode('utf-8'), file=sys.stdout)
    print(proc.stderr.decode('utf-8'), file=sys.stderr)
    return proc.returncode


def create_binary_executable(outpath:str, module_list:List[str], run_exe=False):
    init_llvm_compiler()

    if not isinstance(module_list, (tuple, list)):
        module_list = [ module_list ]

    ret = run_cli_cmd([ 'g++', *module_list, '-o', outpath ])
    assert ret == 0, "Failed to compile modules with g++."

    if run_exe:
        logging.info("Running executable: %s", outpath)
        start_time = datetime.utcnow()

        return_code = run_cli_cmd(outpath)

        end_time = datetime.utcnow()
        logging.info("Executable %s exited with code: %d", outpath, return_code)
        logging.info("Executable %s duration: %s", outpath, end_time - start_time)


def is_primitive_ptr(t):
    if not t.type.is_pointer:
        return False   # not a pointer to anything
    p = t.type.pointee
    prim_types = (ll.IntType, ll.HalfType, ll.FloatType, ll.DoubleType)
    # Pointer to primitive type
    if isinstance(p, prim_types):
        return True
    # Pointer to a constant primitive type
    if isinstance(p, ll.Constant) and isinstance(p.constant, prim_types):
        return True
    return False

