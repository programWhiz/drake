import os
import subprocess
from typing import List
from collections import OrderedDict
import llvmlite.ir as ll
from src import llvm_cast
from src.llvm_cast import llvm_type_shortname
from src.llvm_utils import compile_module_llvm, create_binary_executable, build_main_method, is_primitive_ptr
from src.exceptions import *

int_precisions = {
    'int8': 8,
    'int16': 16,
    'int32': 32,
    'int64': 64,
}

float_precisions = {
    'float16': 16,
    'float32': 32,
    'float64': 64,
}

dtype_to_ir_type = {
    'bool': ll.IntType(8),
    'int8': ll.IntType(8),
    'int16': ll.IntType(16),
    'int32': ll.IntType(32),
    'int64': ll.IntType(64),
    'float32': ll.FloatType(),
    'float64': ll.DoubleType(),
}

int_types = set(int_precisions.keys())
float_types = set(float_precisions.keys())
numeric_types = int_types | float_types
builtin_types = numeric_types | { 'bool', 'none' }

builtin_id = {
    'none': 0,
    'bool': 1,
    'int8': 2,
    'int16': 3,
    'int32': 4,
    'int64': 5,
    'float32': 6,
    'float64': 7
}

id_to_builtin = { v: k for k, v in builtin_id.items() }

arith_ops_matrix = [
    # n   b    i8  i16  i32  i64  f32  f64
    [-1, -1,  -1, -1,  -1,  -1,   -1, -1],  # none
    [-1,  2,   2,  3,   4,   5,    6,  7],  # bool
    [-1,  2,   2,  3,   4,   5,    6,  7],  # i7
    [-1,  3,   3,  3,   4,   5,    6,  7],  # i16
    [-1,  4,   4,  4,   4,   5,    6,  7],  # i32
    [-1,  5,   5,  5,   5,   5,    7,  7],  # i64
    [-1,  6,   6,  6,   6,   7,    6,  7],  # f32
    [-1,  7,   7,  7,   7,   7,    7,  7],  # f64
]

def float_for_precision(bits):
    if bits >= 64:
        return 'float64'
    else:
        return 'float32'


def int_for_precision(bits):
    if bits > 32:
        return 'int64'
    elif bits > 16:
        return 'int32'
    elif bits > 8:
        return 'int16'
    else:
        return 'int8'


class TypeSpec():
    def __init__(self, dtype=None, is_const=False):
        self.dtype = dtype
        self.is_const = is_const

    def __str__(self):
        dtype = str(self.dtype)
        const = "const " if self.is_const else ""

        return f"{const}{dtype}"

    def is_builtin(self):
        return self.dtype in builtin_types

    def builtin_id(self):
        return builtin_id[ self.dtype ]

    @classmethod
    def from_builtin_id(cls, id_, is_const=False):
        return TypeSpec(id_to_builtin[ id_ ], is_const=is_const)

    def is_numeric(self):
        return self.dtype in numeric_types

    def is_float(self):
        return self.dtype in float_types

    def is_int(self):
        return self.dtype in int_types

    def is_boolean(self):
        return self.dtype == 'bool'

    def is_none(self):
        return self.dtype == 'none'

    def subsumes(self, other_type):
        return self.dtype == other_type.dtype

    def equivalent(self, other_type):
        return other_type and self.dtype == other_type.dtype

    def get_llvm_type(self):
        ir_type = dtype_to_ir_type.get(self.dtype)
        if ir_type:
            return ir_type
        raise TypeError(f"Could not compile type '{self.dtype}' to native.")

    def get_llvm_name(self):
        return llvm_type_shortname.get(self.dtype, self.dtype)


class AnyType(TypeSpec):
    def __init__(self):
        super().__init__("any", True)

    def __str__(self):
        return "any"

    def subsumes(self, other_type):
        return True

    def get_llvm_type(self):
        return ll.PointerType(ll.VoidType())

    def get_llvm_name(self):
        return "any"


class UnionSpec(TypeSpec):
    """Represents a type that can be any of the given type specs."""
    def __init__(self, type_specs, **kwargs):
        super().__init__(**kwargs)
        self.type_specs = type_specs

    def __str__(self):
        return '|'.join(str(t) for t in self.type_specs)

    @classmethod
    def as_union(cls, type_spec):
        if isinstance(type_spec, UnionSpec):
            return type_spec
        return UnionSpec(type_specs=[ type_spec ])

    def add_type(self, type_spec):
        if isinstance(type_spec, UnionSpec):
            self.type_specs.extend(type_spec.type_specs)
        else:
            self.type_specs.append(type_spec)

    @classmethod
    def as_single(cls, type_spec):
        if isinstance(type_spec, UnionSpec) and len(type_spec.type_specs) == 1:
            return type_spec.type_specs[0]
        return type_spec

    def subsumes(self, other_type):
        return any(t.subsumes(other_type) for t in self.type_specs)

    def equivalent(self, other_type):
        return isinstance(other_type, UnionSpec) and \
            len(other_type.type_specs) == self.type_specs and \
            all(t.equivalent(t2) for t, t2 in zip(other_type.type_specs, self.type_specs))

    def get_llvm_name(self):
        return ','.join(t.get_llvm_name() for t in self.type_specs)


class ClassSpec(TypeSpec):
    def __init__(self, class_def=None, tpl_params=None, **kwargs):
        super().__init__(**kwargs)
        self.class_def = class_def
        self.dtype = class_def.name
        self.tpl_params = tpl_params or OrderedDict()
        self.llvm_struct = None

    def __str__(self):
        s = super().__str__()
        tpl = ', '.join(f"{k}:{v}" for k, v in self.tpl_params.items())
        s += f'<{tpl}>'
        return s

    def equivalent(self, other):
        return (other and isinstance(other, ClassSpec) and
            other.class_def == self.class_def and
            len(self.tpl_params) == len(other.tpl_params) and
            all(param.equivalent(other.tpl_params[k]) for k, param in self.tpl_params.items()))

    def subsumes(self, other):
        return (other and isinstance(other, ClassSpec) and
               (other.class_def == self.class_def or self.class_def.is_super_class(other)) and
               len(self.tpl_params) == len(other.tpl_params) and
               all(param.subsumes(other.tpl_params[k]) for k, param in self.tpl_params.items()))

    def get_llvm_type(self):
        assert self.llvm_struct is not None
        return self.llvm_struct

    def get_llvm_name(self):
        name = self.dtype
        if self.tpl_params:
            name += '_'
            name += "_".join(t.get_llvm_name() for t in self.tpl_params.values())
        return name


class FuncPtrSpec(TypeSpec):
    """Pointer to one of several types of functions.
    We don't know which one will be selected or used."""
    def __init__(self, functions, **kwargs):
        super().__init__(**kwargs)
        self.functions = functions


class Node():
    def __init__(self, type_spec=None):
        self.type_spec = type_spec

    def build_type_spec(self):
        return self.type_spec


class Instruction:
    def build_type_spec(self):
        raise NotImplementedError()


class Literal(Node):
    def __init__(self, value=None, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def __str__(self):
        return f"{self.type_spec}({self.value})"

    def build_llvm_ir(self, bb):
        ir_type = self.type_spec.get_llvm_type()
        return ll.Constant(ir_type, self.value)


class Int8Literal(Literal):
    def __init__(self, value, **kwargs):
        type_spec = TypeSpec(dtype='int8', is_const=True)
        value = int(value)
        super().__init__(type_spec=type_spec, value=value, **kwargs)


class Int16Literal(Literal):
    def __init__(self, value, **kwargs):
        type_spec = TypeSpec(dtype='int16', is_const=True)
        value = int(value)
        super().__init__(type_spec=type_spec, value=value, **kwargs)


class Int32Literal(Literal):
    def __init__(self, value, **kwargs):
        type_spec = TypeSpec(dtype='int32', is_const=True)
        value = int(value)
        super().__init__(type_spec=type_spec, value=value, **kwargs)


class Int64Literal(Literal):
    def __init__(self, value, **kwargs):
        type_spec = TypeSpec(dtype='int64', is_const=True)
        value = int(value)
        super().__init__(type_spec=type_spec, value=value, **kwargs)


class FloatLiteral(Literal):
    def __init__(self, value, **kwargs):
        type_spec = TypeSpec(dtype='float32', is_const=True)
        value = int(value)
        super().__init__(type_spec=type_spec, value=value, **kwargs)


class Float64Literal(Literal):
    def __init__(self, value, **kwargs):
        type_spec = TypeSpec(dtype='float64', is_const=True)
        value = int(value)
        super().__init__(type_spec=type_spec, value=value, **kwargs)


class BoolLiteral(Literal):
    def __init__(self, value, **kwargs):
        type_spec = TypeSpec(dtype='bool', is_const=True)
        value = int(value)
        super().__init__(type_spec=type_spec, value=value, **kwargs)


class NoneLiteral(Literal):
    def __init__(self, value, **kwargs):
        type_spec = TypeSpec(dtype='none', is_const=True)
        value = int(value)
        super().__init__(type_spec=type_spec, value=value, **kwargs)


class BinaryOp(Instruction):
    def __init__(self, left=None, right=None, left_assoc=True, **kwargs):
        super().__init__(**kwargs)
        self.left = left
        self.right = right
        self.left_op_type_spec = None
        self.right_op_type_spec = None
        self.left_assoc = left_assoc
        self.cast_left = None
        self.cast_right = None

    def build_type_spec(self):
        rtypes = self.right.build_type_spec()
        ltypes = self.left.build_type_spec()

        rtypes = UnionSpec.as_union(rtypes)
        ltypes = UnionSpec.as_union(ltypes)

        self.right_op_type_spec = rtypes
        self.left_op_type_spec = ltypes

        out_types = []
        for ltype in ltypes.type_specs:
            for rtype in rtypes.type_specs:
                out_type = self.get_result_type(ltype, rtype)
                out_types.append(out_type)

        if len(out_types) == 1:
            self.type_spec = out_types[0]
        else:
            self.type_spec = UnionSpec(type_specs=out_types)

        return self.type_spec

    def get_result_type(self, ltype : TypeSpec, rtype : TypeSpec) -> TypeSpec:
        raise NotImplementedError()

    def build_llvm_ir(self, bb):
        left = self.left.build_llvm_ir(bb)
        left_val = bb.load(left) if is_primitive_ptr(left) else left

        right = self.right.build_llvm_ir(bb)
        right_val = bb.load(right) if is_primitive_ptr(right) else right

        op = self.build_llvm_ir_op(bb, left_val, right_val)

        if self.cast_left:
            left_val = self.cast_left(bb, left_val)
        elif self.cast_right:
            right_val = self.cast_right(bb, right_val)

        return op(left_val, right_val)

    def build_llvm_ir_op(self, bb, left, right):
        raise NotImplementedError()


class ArithOp(BinaryOp):
    overload_name = None  # Overwrite this

    def get_result_type(self, ltype, rtype) -> TypeSpec:
        if ltype.is_builtin() and rtype.is_builtin():
            return self.get_primitive_result_type(ltype, rtype)
        else:  # get op func like oper_add
            assert self.overload_name, f'Must defined attribute `overload_name` for class `{self.__class__}`'
            right_fn:FuncBindSpec = get_overload_func(ltype, self.overload_name, rtype)
            left_fn:FuncBindSpec = get_overload_func(rtype, self.overload_name, ltype)

            can_use_right = right_fn.ret_type.subsumes(left_fn.ret_type)
            can_use_left = left_fn.ret_type.subsumes(right_fn.ret_type)

            if can_use_right and can_use_left:
                raise AmbiguousOverloadError(
                    f"Found multiple competing functions `{self.overload_name}` for operands of type `{rtype}` and `{ltype}`")
            if not can_use_left and not can_use_right:
                raise InvalidOperationError(
                    f"No operator `{self.overload_name}` for operands of type `{rtype}` and `{ltype}`.")

            func = right_fn if can_use_right else left_fn
            return InvokeFuncInst()

    def primitive_result_type(self, ltype, rtype) -> TypeSpec:
        out_type_id = arith_ops_matrix[ ltype.builtin_id() ][ rtype.builtin_id() ]
        out_type = TypeSpec.from_builtin_id(out_type_id)
        self.type_spec = out_type

        # Should we cast between parts?
        self.cast_left = None
        if not out_type.equivalent(ltype):
            self.cast_left = llvm_cast.cast_types[ltype.dtype][out_type.dtype]

        self.cast_right = None
        if not out_type.equivalent(rtype):
            self.cast_right = llvm_cast.cast_types[rtype.dtype][out_type.dtype]

        return out_type


class BinaryAdd(ArithOp):
    """Binary addition"""
    overload_name = 'oper_add'

    def build_llvm_ir_op(self, bb, left, right):
        if self.type_spec.is_float():
            return bb.fadd
        return bb.add


class BinarySub(ArithOp):
    """Binary subtraction"""
    overload_name = 'oper_sub'

    def build_llvm_ir_op(self, bb, left, right):
        if self.type_spec.is_float():
            return bb.fsub
        return bb.sub


class AssignAtom(BinaryOp):
    def __init__(self, type_spec=None, **kwargs):
        super().__init__(**kwargs)
        self.type_spec = type_spec
        self.binding = None

    def build_type_spec(self):
        right_type = self.right.build_type_spec()
        left_type = self.left.required_type

        if left_type:
            if not left_type.subsumes(right_type):
                raise Exception(f"Cannot assign type {right_type} to expected type {left_type}")
            type_spec = left_type
        else:
            type_spec = right_type
            self.left.set_type_spec(type_spec)

        print(f"{self.left} <= {right_type}")
        self.type_spec = type_spec

        self.cast_right = None
        if not self.type_spec.equivalent(right_type):
            self.cast_right = llvm_cast.cast_types[right_type.dtype][left_type.dtype]

    def build_llvm_ir(self, bb):
        self.build_type_spec()
        if self.type_spec.is_primitive():
            self.build_llvm_primitive(bb)
        else:
            self.build_llvm_reference(bb)

    def build_llvm_primitive(self, bb):
        right = self.right.build_llvm_ir(bb)
        right_val = bb.load(right) if is_primitive_ptr(right) else right

        left = self.left.build_llvm_ir(bb)
        if self.cast_right:
            right_val = self.cast_right(bb, right_val)

        bb.store(right_val, left)

        return left

    def build_llvm_reference(self, bb):
        right = self.right.build_llvm_ir(bb)

        right_val = bb.load(right) if is_primitive_ptr(right) else right

        left = self.left.build_llvm_ir(bb)
        if self.cast_right:
            right_val = self.cast_right(bb, right_val)

        bb.store(right_val, left)

        return left


class Symbol(Node):
    def __init__(self, name=None, required_type=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.required_type = required_type
        self.llvm_var = None

    def __str__(self):
        return self.name

    def set_type_spec(self, type_spec):
        if not (self.type_spec and type_spec.equivalent(self.type_spec)):
            self.type_spec = type_spec
            self.llvm_var = None

    def build_llvm_ir(self, bb):
        ir_type = self.type_spec.get_llvm_type()
        if self.llvm_var is None:
            self.llvm_var = bb.alloca(ir_type)
        return self.llvm_var


class Block(Instruction):
    def __init__(self, instrs=None, parent=None, funcs=None, classes=None, local_vars=None, global_vars=None):
        self.parent = parent
        self.instrs = instrs or []
        self.classes = classes or []
        self.funcs = funcs or []
        self.local_vars = local_vars or OrderedDict()
        self.global_vars = global_vars or OrderedDict()

        for func in self.funcs:
            func.block = self
        for cls in self.classes:
            cls.block = self

    def build_type_spec(self):
        for instr in self.instrs:
            instr.build_type_spec()


class Module(Block):
    def __init__(self, abs_name, abs_path, **kwargs):
        self.abs_name = abs_name
        self.abs_path = abs_path
        super().__init__(**kwargs)
        self.llvm_init_func = None

    def build_llvm_ir(self):
        module = ll.Module()
        self.build_classes_llvm_ir(module)
        self.build_funcs_llvm_ir(module)
        self.build_init_func_llvm_ir(module)
        return module

    def build_classes_llvm_ir(self, module):
        for cls in self.classes:
            cls.build_llvm_ir(module)

    def build_funcs_llvm_ir(self, module):
        for func in self.funcs:
            func.build_llvm_ir(module)

    def build_init_func_llvm_ir(self, module):
        """Constructs the module init function"""
        fntype = ll.FunctionType(ll.VoidType(), [])

        init_func = ll.Function(module, fntype, name=f'$init_module_{self.abs_name}')
        self.llvm_init_func = init_func
        init_func_build = ll.IRBuilder()
        init_func_build.position_at_end(init_func.append_basic_block())

        for instr in self.instrs:
            instr.build_llvm_ir(init_func_build)

        init_func_build.ret_void()
        return module


class FuncParam(Node):
    def __init__(self, name=None, index=None, default_value=None, required_type=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.index = index
        self.default_value = default_value
        self.binding = None
        self.required_type = required_type

    def build_type_spec(self):
        assert self.binding, f"No value was bound for parameter {self.name}"
        self.type_spec = self.binding
        return self.type_spec

    def build_llvm_ir(self, bb):
        func = getattr(bb, 'func')
        return func.args[self.index]


class ReturnStmt(Instruction):
    def __init__(self, ret_value=None, **kwargs):
        super().__init__(**kwargs)
        self.ret_value = ret_value

    def build_type_spec(self):
        self.type_spec = self.ret_value.build_type_spec()
        return self.type_spec

    def build_llvm_ir(self, bb):
        if self.type_spec is None:
            bb.ret_void()

        ret_val = self.ret_value.build_llvm_ir(bb)

        if is_primitive_ptr(ret_val):
            ret_val = bb.load(ret_val)

        bb.ret(ret_val)


class FuncDef(Block):
    def __init__(self, name=None, params=None, return_stmts=None, block=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.params = params or []
        self.return_stmts = return_stmts or []
        self.template_instances = []
        self.bindings:List["FuncBindSpec"] = []
        self.block = block

    def bind_type_spec(self, args, kwargs):
        binding = self.bind_param_args(args, kwargs)

        # Do we already know what type of value would be returned?
        for existing_binding in self.bindings:
            if existing_binding.equivalent(binding):
                self.bindings.append(binding)
                binding.ret_type = existing_binding.ret_type
                return binding

        # We didn't find a binding, solve return type
        binding.apply_bindings()
        self.bind_return_type(binding)
        self.bindings.append(binding)

        return binding

    def bind_return_type(self, binding):
        for instr in self.instrs:
            instr.build_type_spec()

        if len(self.return_stmts) is None:
            binding.ret_type = NoneLiteral()

        elif len(self.return_stmts) == 1:
            binding.ret_type = self.return_stmts[0].build_type_spec()

        else:
            ret_types = [ r.bind_type_spec() for r in self.return_stmts ]
            binding.ret_type = UnionSpec(type_specs=ret_types)

        return binding.ret_type

    def bind_param_args(self, args, kwargs) -> "FuncBindSpec":
        if len(args) > len(self.params):
            raise Exception(f'Function {self.name} takes {len(self.params)} parameters, {len(args)} given.')

        bind_params = OrderedDict()
        used_keys = set()
        for arg_idx, (name, param) in enumerate(self.params.items()):
            param_type, value_type = None, None
            dtype, is_const = None, None

            if param.required_type:
                param_type = param.required_type
                dtype, is_const = param_type.dtype, param_type.is_const

            if param.default_value:
                value = param.default_value
                value_type = value.build_type_spec()
                if param_type and not param_type.subsumes(value_type):
                    raise Exception(f"Default value for parameter '{param.name}' is not of type {value_type}. Found type {param_type}: {value}")
                elif value_type:
                    dtype, is_const = value_type.dtype, value_type.is_const

            bind_params[name] = FuncBindParam(func_param=param, value=value, dtype=dtype)

        def bind_arg(arg, param, arg_idx, kwarg_key):
            nonlocal self, bind_params, used_keys
            arg_type = arg.build_type_spec()

            binding = bind_params[param.name]
            binding.value = arg

            if kwarg_key is not None:
                binding.set_kwarg_key(kwarg_key)
            else:
                binding.set_arg_index(arg_idx)

            used_keys.add(param.name)

            # If param has an explicit type spec, use it
            if param.required_type:
                if not param.required_type.subsumes(arg_type):
                    raise Exception(f"Invoking function `{self.name}`: Cannot cast arg "
                                    f"`{param.name}` from type {arg_type} to {param.required_type}")

            else:  # use arg param type
                binding.dtype = arg_type.dtype

        for arg_idx, (arg, param) in enumerate(zip(args, self.params.values())):
            bind_arg(arg, param, arg_idx, None)

        # Iterate through keyword args
        for key, arg in kwargs.items():
            if key not in self.params:
                raise Exception(f"Invoking function `{self.name}`: No parameter named `{key}`.")
            if key in used_keys:
                raise Exception(f"Invoking function `{self.name}`: Duplicate value for parameter `{key}`.")
            bind_arg(arg, self.params[key], None, key)

        unbound = [ key for key, bind in bind_params.items() if bind.value is None ]
        if unbound:
            missing_names = ", ".join(unbound)
            raise Exception(f"Invoking function `{self.name}`, no value for parameter(s): {missing_names}")

        # Bind params, don't solve return type yet
        return FuncBindSpec(func=self, bind_params=bind_params, ret_type=None)

    def get_llvm_name(self, fntype:ll.FunctionType) -> str:
        name = ""
        if self.parent:
            name = self.parent.get_llvm_name()
            name += '.'
        name += self.name

        name += '_' + fntype.return_type.llvm_type_name()

        if len(fntype.args) > 0:
            name += '_'
            name += '_'.join(arg.llvm_type_name() for arg in fntype.args)

        return name

    def build_llvm_ir(self, module):
        existing_funcs = dict()

        for binding in self.bindings:
            fntype = binding.get_llvm_func_type()
            func_name = self.get_llvm_name(fntype)
            binding.llvm_name = func_name

            if func_name in existing_funcs:
                binding.llvm_func = existing_funcs[func_name]

            # Update the graph nodes to correct type
            binding.apply_bindings()
            self.bind_return_type(binding)

            func = ll.Function(module, fntype, name=func_name)
            block = func.append_basic_block()
            bb = ll.IRBuilder()
            bb.position_at_end(block)

            binding.llvm_func = func
            setattr(bb, 'func', func)
            existing_funcs[func_name] = func

            for instr in self.instrs:
                instr.build_llvm_ir(bb)

            if isinstance(fntype.return_type, ll.VoidType):
                bb.ret_void()


class FuncBindParam(TypeSpec):
    def __init__(self, func_param, value, is_kwarg = False,
                 kwarg_key: str = None, arg_idx : int = None, **kwargs):
        super().__init__(**kwargs)
        self.func_param = func_param
        self.value = value
        self.is_kwarg = is_kwarg
        self.is_idx_arg = not is_kwarg
        self.kwarg_key = kwarg_key
        self.arg_idx = arg_idx

    def set_kwarg_key(self, key:str):
        self.is_kwarg = True
        self.kwarg_key = key
        self.is_arg_idx = False
        self.arg_idx = None

    def set_arg_index(self, idx:int):
        self.is_kwarg = False
        self.kwarg_key = None
        self.is_arg_idx = True
        self.arg_idx = idx

    def build_llvm_ir(self, bb):
        value = self.value.build_llvm_ir(bb)
        return bb.load(value) if is_primitive_ptr(value) else value


class FuncBindSpec(TypeSpec):
    """
    A single instantiation of a function, has a specific arity and list of params.
    """
    def __init__(self, func, bind_params, ret_type, **kwargs):
        super().__init__(**kwargs)
        self.func:FuncDef = func
        self.ret_type = ret_type
        self.bind_params = bind_params
        self.invocations:set["InvokeFunc"] = set()
        self.llvm_func = None
        self.llvm_name = None

    def __str__(self):
        params = ', '.join(f"{k}:{v}" for k, v in self.bind_params.items())
        return f"{self.func}({params}):{self.ret_type}"

    def subsumes(self, func_bind):
        # The two should be identical sets of parameters
        assert set(func_bind.bind_params.keys()) == set(self.bind_params.keys())

        # all params must subsume all params from the other function
        for key in self.bind_params.keys():
            this_param = self.bind_params[key]
            that_param = func_bind.bind_params[key]
            if not this_param.subsumes(that_param):
                return False
        return True

    def equivalent(self, func_bind):
        # The two should be identical sets of parameters
        assert set(func_bind.bind_params.keys()) == set(self.bind_params.keys())

        # all params must subsume all params from the other function
        for key in self.bind_params.keys():
            this_param = self.bind_params[key]
            that_param = func_bind.bind_params[key]
            if not this_param.equivalent(that_param):
                return False
        return True

    def apply_bindings(self):
        for key, bind in self.bind_params.items():
            bind.func_param.binding = bind

    def get_llvm_func_type(self):
        ret_type = self.ret_type.get_llvm_type() if self.ret_type else ll.VoidType()
        return ll.FunctionType(ret_type, [ p.get_llvm_type() for p in self.bind_params.values() ])

    def get_llvm_name(self):
        if self.llvm_name is None:
            self.llvm_name = self.func.get_llvm_name(self.get_llvm_func_type())
        return self.llvm_name

    def get_llvm_func(self):
        return self.llvm_func

    def build_llvm_call(self, bb):
        func_args = [ None ] * len(self.bind_params)
        for param in self.bind_params.values():
            func_args[param.func_param.index] = param.build_llvm_ir(bb)

        ret = bb.call(self.llvm_func, func_args)
        return ret


class InvokeFunc(Instruction):
    def __init__(self, func=None, args=None, kwargs=None, binding=None, **super_kwargs):
        super().__init__(**super_kwargs)
        self.func:FuncDef = func
        self.binding = binding
        self.args = args or []
        self.kwargs = kwargs or {}
        self.type_spec = None

    def build_type_spec(self):
        if self.binding is None:
            self.binding = self.func.bind_type_spec(self.args, self.kwargs)
            self.binding.invocations.add(self)
        print(self.func.name, "<=", self.binding)
        return self.binding.ret_type

    def build_llvm_ir(self, bb):
        val = self.binding.build_llvm_call(bb)
        return val


class ClassDef(Block):
    """Define a class"""
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.instances = []

    def build_type_spec(self):
        return ClassSpec(class_def=self, tpl_params={
            k: v.build_type_spec() for k, v in self.local_vars.items() })

    def build_llvm_ir(self, module:ll.Module):
        existing = dict()

        for inst in self.instances:
            type:ClassSpec = inst.type_spec
            bind_name = type.get_llvm_name()

            struct = existing.get(bind_name)
            if not struct:
                struct_elems = [p.get_llvm_type() for p in type.tpl_params.values()]
                struct = module.context.get_identified_type(bind_name)
                struct.set_body(*struct_elems)
                existing[bind_name] = struct

            inst.llvm_class = struct
            inst.type_spec.llvm_struct = struct


class InstClass(Instruction):
    """Instantiation of a class"""
    def __init__(self, class_def, ctor_args=None, **kwargs):
        super().__init__(**kwargs)
        self.class_def = class_def
        self.class_def.instances.append(self)
        self.ctor_args = ctor_args or {}
        self.llvm_class = None  # class built in "build classes" step of module
        self.llvm_cls_inst = None  # instantiated class in llvm

    def build_type_spec(self):
        # self.class_def.bind_params(self.bind_params)
        class_spec = self.class_def.build_type_spec()
        # overwrite the types of any bind vars
        for k, v in self.ctor_args.items():
            class_spec.tpl_params[k] = v.build_type_spec()
        self.type_spec = class_spec
        return self.type_spec

    def build_llvm_ir(self, bb):
        # TODO: malloc or make smart ptr here?
        if self.llvm_cls_inst is None:
            self.llvm_cls_inst = bb.alloca(self.llvm_class)
        return self.llvm_cls_inst


class GetAttr(Instruction):
    def __init__(self, block, attr_name, **kwargs):
        super().__init__(**kwargs)
        self.block = block
        self.attr_name = attr_name

    def build_type_spec(self):
        attr = self.block.get_attr(self.attr_name)
        self.type_spec = attr.build_type_spec()
        print("Get attr:", self.attr_name, "<=", type_spec)
        return

    def build_llvm_ir(self, bb):
        val = self.binding.build_llvm_call(bb)
        return val


def test():
    pair_class = ClassDef(
        name="Pair", local_vars={ 'a': Symbol(name='a'), 'b': Symbol(name='b') })

    pair = Symbol(name='pair')
    pair2 = Symbol(name='pair2')

    inst_pair = InstClass(pair_class, ctor_args={
        'a': Int32Literal(value=6), 'b': Int32Literal(value=10) })

    ass_pair = AssignAtom(left=pair, right=inst_pair)

    inst_pair = InstClass(pair_class, ctor_args={
        'a': FloatLiteral(value=3.1415), 'b': FloatLiteral(value=1.234) })

    ass_pair2 = AssignAtom(left=pair2, right=inst_pair)
    # ass_pair_a = AssignAtom(left=GetAttr(pair, 'a'), right=Int32Literal(100))
    # ass_pair_b = AssignAtom(left=GetAttr(pair, 'b'), right=Int32Literal(256))

    # add_xy = BinaryAdd(left=x, right=GetAttr(pair, 'a'))
    #
    # z = Symbol(name='z')
    # ass_z = AssignAtom(left=z, right=add_xy)

    # fn subtract(a, b): return a - b;
    # param_a = FuncParam(name='a', default_value=Int32Literal(1), index=0)
    # param_b = FuncParam(name='b', index=1)
    # a_minus_b = BinarySub(left=param_a, right=param_b)
    # c = Symbol(name='c')
    # ass_c = AssignAtom(left=c, right=a_minus_b)
    # return_c = ReturnStmt(c)
    #
    # subtract = FuncDef(
    #     name='subtract',
    #     params=OrderedDict(a=param_a, b=param_b),
    #     instrs=[ ass_c, return_c ],
    #     return_stmts=[ return_c ])
    #
    # w = Symbol(name='w')
    #
    # ass_w = AssignAtom(left=w, right=InvokeFunc(
    #     func=subtract,
    #     args=[z, y],
    # ))
    #
    # ass_w2 = AssignAtom(left=w, right=InvokeFunc(func=subtract, args=[ Int32Literal(3), FloatLiteral(4) ]))

    module = Module(abs_name='__main__', abs_path=__file__,
                    funcs=[],
                    classes=[ pair_class ],
                    instrs=[ ass_pair, ass_pair2 ])

    module.build_type_spec()

    print("=== IR Code ===\n\n")
    llvm_module = module.build_llvm_ir()

    print(str(llvm_module))

    # We need a main method as entry point
    build_main_method(llvm_module, module.llvm_init_func)
    obj_file = compile_module_llvm("/tmp/tmp.dk", llvm_module)
    create_binary_executable("/tmp/tmp.exe", [ obj_file ], run_exe=True)


if __name__ == '__main__':
    test()
