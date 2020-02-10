from typing import List
from collections import OrderedDict

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
    'float16': 6,
    'float32': 7,
    'float64': 8
}

id_to_builtin = { v: k for k, v in builtin_id.items() }

arith_ops_matrix = [
    # n   b    i8  i16  i32  i64  f16  f32  f64
    [-1, -1,  -1, -1,  -1,  -1,   -1,  -1, -1],  # none
    [-1,  2,   2,  3,   4,   5,    6,   7,  8],  # bool
    [-1,  2,   2,  3,   4,   5,    6,   7,  8],  # i8
    [-1,  3,   3,  3,   4,   5,    7,   7,  8],  # i16
    [-1,  4,   4,  4,   4,   5,    7,   7,  8],  # i32
    [-1,  5,   5,  5,   5,   5,    8,   8,  8],  # i64
    [-1,  6,   6,  7,   7,   8,    6,   7,  8],  # f16
    [-1,  7,   7,  7,   7,   8,    7,   7,  8],  # f32
    [-1,  8,   8,  8,   8,   8,    8,   8,  8],  # f64
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


class AnyType(TypeSpec):
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


class IntLiteral(Literal):
    def __init__(self, value, **kwargs):
        type_spec = TypeSpec(dtype='int32', is_const=True)
        value = int(value)
        super().__init__(type_spec=type_spec, value=value, **kwargs)


class FloatLiteral(Literal):
    def __init__(self, value, **kwargs):
        type_spec = TypeSpec(dtype='float32', is_const=True)
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
    def __init__(self, left=None, right=None, **kwargs):
        super().__init__(**kwargs)
        self.left = left
        self.right = right


    def build_type_spec(self):
        rtypes = self.right.build_type_spec()
        ltypes = self.left.build_type_spec()

        rtypes = UnionSpec.as_union(rtypes)
        ltypes = UnionSpec.as_union(ltypes)

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


class ArithOp(BinaryOp):
    def get_result_type(self, ltype, rtype) -> TypeSpec:
        if ltype.is_builtin() and rtype.is_builtin():
            out_id = arith_ops_matrix[ ltype.builtin_id() ][ rtype.builtin_id() ]
            return TypeSpec.from_builtin_id(out_id)
        else:
            raise NotImplemented("No operator for non-built-in types.")


class BinaryAdd(ArithOp):
    """Binary addition"""
    pass


class BinarySub(ArithOp):
    """Binary subtraction"""
    pass

class AssignAtom(BinaryOp):
    def __init__(self, type_spec=None, **kwargs):
        super().__init__(**kwargs)
        self.type_spec = type_spec

    def build_type_spec(self):
        right_type = self.right.build_type_spec()
        if self.type_spec and not self.type_spec.is_compatible(right_type):
            raise Exception(f"Cannot assign type {right_type} to expected type {self.type_spec}")
        print(f"{self.left} <= {right_type}")
        self.left.type_spec = right_type
        return self.left.type_spec


class Symbol(Node):
    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def __str__(self):
        return self.name

class Block(Instruction):
    def __init__(self, instrs=[], parent=None, scope_vars={}):
        self.parent = parent
        self.instrs = instrs
        self.scope_vars = {}

    def build_type_spec(self):
        for instr in self.instrs:
            instr.build_type_spec()


class Module(Block):
    pass


class FuncParam(Node):
    def __init__(self, name=None, index=None, default_value=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.index = index
        self.default_value = default_value
        self.binding = None

    def build_type_spec(self):
        assert self.binding, f"No value was bound for parameter {self.name}"
        return self.binding


class ReturnStmt(Instruction):
    def __init__(self, ret_value=None, **kwargs):
        super().__init__(**kwargs)
        self.ret_value = ret_value

    def build_type_spec(self):
        return self.ret_value.build_type_spec()


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

        for existing_binding in self.bindings:
            if existing_binding.subsumes(binding):
                return existing_binding

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

            if param.type_spec:
                param_type = param.type_spec
                dtype, is_const = param_type.dtype, param_type.is_const

            if param.default_value:
                value = param.default_value
                value_type = value.build_type_spec()
                if param_type and not param_type.subsumes(value_type):
                    raise Exception(f"Default value for parameter '{param.name}' is not of type {param_type}. Found type {value_type}: {value}")
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
            if param.type_spec:
                if not param.type_spec.subsumes(arg_type):
                    raise Exception(f"Invoking function `{self.name}`: Cannot cast arg "
                                    f"`{param.name}` from type {arg_type} to {param.type_spec}")

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

    def apply_bindings(self):
        for key, bind in self.bind_params.items():
            bind.func_param.binding = bind


class InvokeFunc(Instruction):
    def __init__(self, func=None, args=None, kwargs=None, **super_kwargs):
        super().__init__(**super_kwargs)
        self.func:FuncDef = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.type_spec = None

    def build_type_spec(self):
        self.binding = self.func.bind_type_spec(self.args, self.kwargs)
        return self.binding.ret_type


x = Symbol(name='x')
ass_x = AssignAtom(left=x, right=BoolLiteral(True))

y = Symbol(name='y')
ass_y = AssignAtom(left=y, right=BoolLiteral(True))

add_xy = BinaryAdd(left=x, right=y)
z = Symbol(name='z')
ass_z = AssignAtom(left=z, right=add_xy)

# fn subtract(a, b): return a - b;
param_a = FuncParam(name='a', default_value=IntLiteral(1))
param_b = FuncParam(name='b')
a_minus_b = BinarySub(left=param_a, right=param_b)
c = Symbol(name='c')
ass_c = AssignAtom(left=c, right=a_minus_b)
return_c = ReturnStmt(c)

subtract = FuncDef(
    name='subtract',
    params=OrderedDict(a=param_a, b=param_b),
    instrs=[ ass_c, return_c ],
    return_stmts=[ return_c ])

# w = subtract(z, y)
w = Symbol(name='w')
invoke_subtract = InvokeFunc(
    func=subtract,
    args=[z],
    kwargs={'b': y},
)
ass_w = AssignAtom(left=w, right=invoke_subtract)
ass_w2 = AssignAtom(left=w, right=InvokeFunc(func=subtract, args=[ IntLiteral(3), FloatLiteral(4) ]))

module = Module(instrs=[ ass_x, ass_y, ass_z, ass_w, ass_w2 ])
module.build_type_spec()
