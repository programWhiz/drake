import sys
from multimethod import overload
import llvmlite.ir as ll
from src.exceptions import *
from src.llvm_ast import next_id, INTRINSIC_FUNC_NAMES


def compile_hl_ast(module, is_main=False):
    ll_mod = {
        'name': module['name'],
        'funcs': [],
        'classes': []
    }

    scope = { 'll_mod': ll_mod, 'hl_mod': module, 'scope': [] }

    init_func = push_scope(scope, f"{module['name']}.$init")
    push_module_idempotency_instr(scope)

    for instr in module['instrs']:
        compile_hl_instr(instr, scope)

    push_instr(scope, { 'op': 'ret_void' })

    # add the init func to the module
    init_func = {
        "name": init_func['name'],
        "args": [],
        "ret": { "type": ll.VoidType() },
        "id": next_id(),
        "instrs": init_func['instrs']
    }

    ll_mod['funcs'].append(init_func)

    if is_main:
        push_module_main(ll_mod, init_func)

    return ll_mod


def push_module_main(ll_mod, init_func):
    argc = ll.IntType(32)
    argv = ll.PointerType(ll.PointerType(ll.IntType(8)))
    ll_mod['funcs'].append({
        'name': 'main',
        'ret': { 'type': ll.IntType(32) },
        'args': [ { 'type': argc }, { 'type': argv } ],
        'instrs': [
            {
                'op': 'call',
                'func': { "id": init_func['id'] },
                'args': []
            },
            { 'op': 'ret', 'value': { 'op': 'const_val', 'value': ll.Constant(ll.IntType(32), 0) } }
        ]
    })


def push_module_idempotency_instr(scope):
    i1 = ll.IntType(8)
    zero, one = ll.Constant(i1, 0), ll.Constant(i1, 1)

    # declare global is_module_init = False
    global_instr = push_instr(scope, {
        'op': 'global_var',
        'align': 1,
        'name': '$module.is_init',
        'type': i1,
        'value': zero,
    })

    ref = { 'id': global_instr['id'] }

    # if is_module_init:
    #   return
    # else:
    #   is_module_init = true
    push_instr(scope, {
        'op': 'if',
        'cond': {
            'op': 'trunc', 'type': ll.IntType(1), 'value': { 'op': 'load', 'ref': ref },
        },
        'true': [{ 'op': 'ret_void' }],
        'false': [{
            'op': 'store',
            'ref': ref,
            'value': { 'op': 'const_val', 'type': i1, 'value': one }
        }]
    })


def push_scope(scope, new_scope_name:str, is_global:bool=False):
    s = { "name": new_scope_name, "instrs": [], "is_global": is_global }
    # if this is top level scope, then its a global scope
    scope['scope'].append(s)
    return s


def push_instr(scope, instr):
    if not instr.get('id'):
        instr['id'] = next_id()
    scope['scope'][-1]['instrs'].append(instr)
    return instr


def pop_scope(scope):
    if len(scope['scope']) == 0:
        raise BuildException("Attempt to pop empty scope stack.")

    return scope['scope'].pop()


@overload
def compile_hl_instr(ast, scope):
    print("[ERROR] unsupported ast node:", ast, file=sys.stderr)
    raise Exception("Unsupported ast node " + ast.get('op'))


def is_op(op_name):
    return lambda ast: isinstance(ast, dict) and ast.get('op') == op_name


def get_local_instr_list(scope):
    local = scope['local_scope']
    while local:
        if 'instrs' in local:
            return local['instrs']
        local = local.get('parent')
    raise Exception("Could not find local block with instruction list.")


@overload
def compile_hl_instr(ast:is_op('printf'), scope):
    args = [ compile_hl_instr(arg, scope) for arg in ast['args'] ]
    return push_instr(scope, { 'op': 'call', 'intrinsic': 'printf', 'args': args })


@overload
def compile_hl_instr(ast:is_op('add'), scope):
    left = compile_hl_ast(ast['left'], scope)
    right = compile_hl_ast(ast['right'], scope)

    left_type = get_instr_type(ast['left'], left, scope)
    right_type = get_instr_type(ast['right'], right, scope)

    if is_numeric(left_type) and is_numeric(right_type):
        out_type = get_min_numeric_precision(left_type, right_type)

    return {
        'type': out_type,
    }


def is_literal_instr(instr):
    return isinstance(instr, dict) and instr.get('literal') is True


def is_numeric_instr(instr):
    return is_literal_instr(instr) and instr['type'] == 'numeric'


def is_str_literal_instr(instr):
    return is_literal_instr(instr) and instr['type'] == 'str'


@overload
def compile_hl_instr(ast:is_str_literal_instr, scope):
    return { 'op': 'const_str', 'value': ast['value'] }


@overload
def compile_hl_instr(ast:is_numeric_instr, scope):
    subtype = ast['subtype']
    precision = ast['precision']

    if subtype == 'int':
        return ll.IntType(precision)
    elif subtype == 'float':
        if precision == 16:
            return ll.HalfType()
        elif precision == 32:
            return ll.FloatType()
        elif precision == 64:
            return ll.DoubleType()
    elif subtype == 'bool':
        return ll.IntType(1)
    else:
        print(f"[ERROR] Unhandled numeric literal type:", ast)
        raise BuildException("Unhandled numeric type: " + ast['subtype'])


def make_int(value, precision=32):
    return {
        "literal": True,
        "type": "numeric",
        "subtype": "int",
        "precision": precision,
        "value": value
    }


def make_float(value, precision=32):
    return {
        "literal": True,
        "type": "numeric",
        "subtype": 'float',
        "precision": precision,
        "value": value
    }


def make_bool(value):
    return {
        "literal": True,
        "type": "numeric",
        "subtype": "bool",
        "precision": 1,
        "value": value
    }


def make_str(value):
    return {
        "literal": True,
        "type": "str",
        "value": value
    }
