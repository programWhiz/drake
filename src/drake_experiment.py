import os
import subprocess
from typing import List
from collections import OrderedDict
import llvmlite.ir as ll
from src.llvm_utils import compile_module_llvm, create_binary_executable

int_precisions = {
    'int8': 8,
    'int16': 16,
    'int32': 32,
    'int64': 64,
}

float_precisions = {
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
        return self.dtype == other_type.dtype

    def get_ir_type(self):
        ir_type = dtype_to_ir_type.get(self.dtype)
        if ir_type:
            return ir_type
        raise f"Could not compile type '{self.dtype}' to native."


class AnyType(TypeSpec):
    def __init__(self):
        super().__init__("any", True)

    def __str__(self):
        return "any"

    def subsumes(self, other_type):
        return True


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


class ClassSpec(TypeSpec):
    def __init__(self, tpl_params=None, **kwargs):
        super().__init__(**kwargs)
        self.tpl_params = tpl_params or []

    def __str__(self):
        s = super().__str__()
        tpl = ', '.join(f"{k}:{v}" for k, v in self.tpl_params.items())
        s += f'<{tpl}>'
        return s


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
        assert self.type_spec
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
        ir_type = self.type_spec.get_ir_type()
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
        left_val = bb.load(left) if left.type.is_pointer else left

        right = self.right.build_llvm_ir(bb)
        right_val = bb.load(right) if right.type.is_pointer else right

        return self.build_llvm_ir_op(bb, left_val, right_val)

    def build_llvm_ir_op(self, bb, left, right):
        raise NotImplementedError()


class ArithOp(BinaryOp):
    def get_result_type(self, ltype, rtype) -> TypeSpec:
        if ltype.is_builtin() and rtype.is_builtin():
            out_id = arith_ops_matrix[ ltype.builtin_id() ][ rtype.builtin_id() ]
            return TypeSpec.from_builtin_id(out_id)
        else:
            raise NotImplemented("No operator for non-built-in types.")


class BinaryAdd(ArithOp):
    """Binary addition"""
    def build_llvm_ir_op(self, bb, left, right):
        return bb.add(left, right)


class BinarySub(ArithOp):
    """Binary subtraction"""
    def build_llvm_ir_op(self, bb, left, right):
        return bb.sub(left, right)


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
            self.left.type_spec = type_spec

        print(f"{self.left} <= {right_type}")
        self.type_spec = type_spec

    def build_llvm_ir(self, bb):
        right = self.right.build_llvm_ir(bb)
        right_val = bb.load(right) if right.type.is_pointer else right
        left = self.left.build_llvm_ir(bb)
        bb.store(right_val, left)
        return left


class Symbol(Node):
    def __init__(self, name=None, required_type=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.required_type = required_type

    def __str__(self):
        return self.name

    def build_llvm_ir(self, bb):
        ir_type = self.type_spec.get_ir_type()
        stack_var = bb.alloca(ir_type)
        return stack_var


class Block(Instruction):
    def __init__(self, instrs=[], parent=None, scope_vars={}):
        self.parent = parent
        self.instrs = instrs
        self.scope_vars = {}

    def build_type_spec(self):
        for instr in self.instrs:
            instr.build_type_spec()


class Module(Block):
    def __init__(self, abs_name, abs_path, **kwargs):
        self.abs_name = abs_name
        self.abs_path = abs_path
        super().__init__(**kwargs)

    def build_llvm_ir(self):
        module = ll.Module()

        fntype = ll.FunctionType(ll.VoidType(), [])

        module_code_name = self.abs_name.replace('.', '_')
        init_func = ll.Function(module, fntype, name=f'init_module_{module_code_name}')
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


class ReturnStmt(Instruction):
    def __init__(self, ret_value=None, **kwargs):
        super().__init__(**kwargs)
        self.ret_value = ret_value

    def build_type_spec(self):
        self.type_spec = self.ret_value.build_type_spec()
        return self.type_spec


class FuncDef(Block):
    def __init__(self, name=None, params=None, return_stmts=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.params = params or []
        self.return_stmts = return_stmts or []
        self.template_instances = []
        self.bindings:List["FuncBindSpec"] = []

    def bind_type_spec(self, args, kwargs):
        binding = self.bind_param_args(args, kwargs)

        # Do we already know what type of value would be returned?
        for existing_binding in self.bindings:
            if existing_binding.equivalent(binding):
                binding.ret_type = existing_binding.ret_type
                return binding

        binding.apply_bindings()

        # We didn't find a binding, solve return type
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
        for name, param in self.params.items():
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

        def bind_arg(arg, param):
            nonlocal self, bind_params, used_keys
            arg_type = arg.build_type_spec()

            binding = bind_params[param.name]
            binding.value = arg
            used_keys.add(param.name)

            # If param has an explicit type spec, use it
            if param.required_type:
                if not param.required_type.subsumes(arg_type):
                    raise Exception(f"Invoking function `{self.name}`: Cannot cast arg "
                                    f"`{param.name}` from type {arg_type} to {param.required_type}")

            else:  # use arg param type
                binding.dtype = arg_type.dtype

        for arg, param in zip(args, self.params.values()):
            bind_arg(arg, param)

        # Iterate through keyword args
        for key, arg in kwargs.items():
            if key not in self.params:
                raise Exception(f"Invoking function `{self.name}`: No parameter named `{key}`.")
            if key in used_keys:
                raise Exception(f"Invoking function `{self.name}`: Duplicate value for parameter `{key}`.")
            bind_arg(arg, self.params[key])

        unbound = [ key for key, bind in bind_params.items() if bind.value is None ]
        if unbound:
            missing_names = ", ".join(unbound)
            raise Exception(f"Invoking function `{self.name}`, no value for parameter(s): {missing_names}")

        # Bind params, don't solve return type yet
        return FuncBindSpec(func=self, bind_params=bind_params, ret_type=None)


    def build_llvm_ir(self, module):
        for binding in self.bindings:
            func = ll.Function(module, fntype, name='foo')
            block = func.append_basic_block()
            bb = ll.IRBuilder()
            bb.position_at_end(block)

            for instr in self.instrs:
                instr.build_llvm_ir(bb)


class FuncBindParam(TypeSpec):
    def __init__(self, func_param, value, **kwargs):
        super().__init__(**kwargs)
        self.func_param = func_param
        self.value = value


class FuncBindSpec(TypeSpec):
    """
    A single instantiation of a function, has a specific arity and list of params.
    """
    def __init__(self, func, bind_params, ret_type, **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.ret_type = ret_type
        self.bind_params = bind_params
        self.invocations:set["InvokeFunc"] = set()

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

    def get_llvm_func_spec(self):
        ret_type = self.ret_type.get_llvm_ir() if self.ret_type else ll.VoidType()
        return ll.FunctionType(ret_type, [ p.get_llvm_ir() for p in self.bind_params ])


class InvokeFunc(Instruction):
    def __init__(self, func=None, args=None, kwargs=None, **super_kwargs):
        super().__init__(**super_kwargs)
        self.func:FuncDef = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.type_spec = None

    def build_type_spec(self):
        self.binding = self.func.bind_type_spec(self.args, self.kwargs)
        self.binding.invocations.add(self)
        return self.binding.ret_type

    def get_llvm_ir(self):
        pass


x = Symbol(name='x')
ass_x = AssignAtom(left=x, right=BoolLiteral(True))

y = Symbol(name='y')
ass_y = AssignAtom(left=y, right=BoolLiteral(True))

add_xy = BinaryAdd(left=x, right=y)
z = Symbol(name='z')
ass_z = AssignAtom(left=z, right=add_xy)

# fn subtract(a, b): return a - b;
# param_a = FuncParam(name='a', default_value=Int32Literal(1))
# param_b = FuncParam(name='b')
# a_minus_b = BinarySub(left=param_a, right=param_b)
# c = Symbol(name='c')
# ass_c = AssignAtom(left=c, right=a_minus_b)
# return_c = ReturnStmt(c)

# subtract = FuncDef(
#     name='subtract',
#     params=OrderedDict(a=param_a, b=param_b),
#     instrs=[ ass_c, return_c ],
#     return_stmts=[ return_c ])
#
# w = subtract(z, y)
# w = Symbol(name='w')
# invoke_subtract = InvokeFunc(
#     func=subtract,
#     args=[z],
#     kwargs={'b': y},
# )
# ass_w = AssignAtom(left=w, right=invoke_subtract)
# ass_w2 = AssignAtom(left=w, right=InvokeFunc(func=subtract, args=[ Int32Literal(3), FloatLiteral(4) ]))

module = Module(abs_name='__main__', abs_path=__file__,
                # funcs=[ subtract ],
                instrs=[ ass_x, ass_y, ass_z ])
module.build_type_spec()

print("=== IR Code ===\n\n")
llvm_module = module.build_llvm_ir()

print(str(llvm_module))

obj_file = compile_module_llvm("/tmp/tmp.dk", llvm_module)
create_binary_executable("/tmp/tmp.exe", [ obj_file ])
