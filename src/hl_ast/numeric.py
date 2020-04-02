import llvmlite.ir as ll
from .type import Type


class NumericType(Type):
    __slots__ = ['is_int', 'signed_int', 'is_bool',
                 'precision', 'strict_subtype', 'strict_precision']

    def __init__(self,
                 is_int: bool = True,
                 signed_int: bool = True,
                 precision: int = 32,
                 is_bool: int = False,
                 strict_subtype: bool = False,
                 strict_precision: bool = False,
                 **kwargs):
        super().__init__(**kwargs)
        self.is_int = is_int
        self.signed_int = signed_int
        self.is_bool = is_bool
        self.precision = precision
        self.strict_subtype = strict_subtype
        self.strict_precision = strict_precision

    def with_props(self, **props):
        return NumericType(
            is_int=props.get('is_int', self.is_int),
            signed_int=props.get('signed_int', self.signed_int),
            is_bool=props.get('is_bool', self.is_bool),
            precision=props.get('precision', self.precision),
            strict_subtype=props.get('strict_subtype', self.strict_subtype),
            strict_precision=props.get('strict_precision', self.strict_precision))

    def with_precision(self, p):
        return self.with_props(precision=p)

    def equivalent(self, other):
        if not isinstance(other, NumericType):
            return False

        return self.is_int == other.is_int and \
               self.signed_int == other.signed_int and \
               self.is_bool == other.is_bool and \
               self.precision == other.precision

    def to_tuple(self):
        return (self.shortname(),)

    def shortname(self):
        if self.is_bool:
            return 'b'
        elif self.is_int:
            if self.signed_int:
                return f'i{self.precision}'
            return f'u{self.precision}'
        else:
            return f'f{self.precision}'

    def longname(self):
        if self.is_bool:
            return 'bool'
        elif self.is_int:
            if self.signed_int:
                return f'int{self.precision}'
            return f'uint{self.precision}'
        else:
            return f'float{self.precision}'

    def ll_type(self):
        if self.is_int:
            return ll.IntType(self.precision)
        elif self.is_bool:
            return ll.IntType(8)

        if self.precision >= 64:
            return ll.DoubleType()
        elif self.precision >= 32:
            return ll.FloatType()
        elif self.precision >= 16:
            return ll.HalfType()

    def is_primitive(self):
        return True

    def can_cast_to(self, other):
        return isinstance(other, NumericType) and other.is_int == self.is_int

    def get_cast_op(self, other):
        if other.precision < self.precision:
            pass
        return numeric_cast_ops[self.shortname()][other.shortname()]

    def get_float_cast(self, other):
        if not self.is_int:
            return None
        return numeric_cast_ops[self.shortname()][other.shortname()]

    def cpp_type(self):
        if self.is_int:
            if not self.signed_int:
                return f'uint{self.precision}_t'
            return f'int{self.precision}_t'
        else:
            if self.precision == 32:
                return 'float'
            elif self.precision == 64:
                return 'double'
            else:
                return 'long double'


class BoolType(NumericType):
    def __init__(self):
        super().__init__(
            is_bool=True,
            is_int=True,
            precision=8,
            signed_int=False
        )

    def cpp_type(self):
        return 'bool'


class BitType(NumericType):
    def __init__(self):
        super().__init__(
            is_bool=True,
            is_int=True,
            precision=1,
            signed_int=False
        )

    def cpp_type(self):
        return 'bool'


numeric_cast_ops = {
    'i8': {
        'i8': None, 'i16': 'sext', 'i32': 'sext', 'i64': 'sext',
        'u8': None, 'u16': 'zext', 'u32': 'zext', 'u64': 'zext',
        'f32': 'sitofp', 'f64': 'sitofp',
    },
    'i16': {
        'i8': 'trunc', 'i16': None, 'i32': 'sext', 'i64': 'sext',
        'u8': 'trunc', 'u16': None, 'u32': 'zext', 'u64': 'zext',
        'f32': 'sitofp', 'f64': 'sitofp',
    },
    'i32': {
        'i8': 'trunc', 'i16': 'trunc', 'i32': None, 'i64': 'sext',
        'u8': 'trunc', 'u16': 'trunc', 'u32': None, 'u64': 'zext',
        'f32': 'sitofp', 'f64': 'sitofp',
    },
    'i64': {
        'i8': 'trunc', 'i16': 'trunc', 'i32': 'trunc', 'i64': None,
        'u8': 'trunc', 'u16': 'trunc', 'u32': 'trunc', 'u64': None,
        'f32': 'sitofp', 'f64': 'sitofp',
    },
    'f32': {
        'i8': 'fptosi', 'i16': 'fptosi', 'i32': 'fptosi', 'i64': 'fptosi',
        'u8': 'fptoui', 'u16': 'fptoui', 'u32': 'fptoui', 'u64': 'fptoui',
        'f32': None, 'f64': 'fpext',
    },
    'f64': {
        'i8': 'fptosi', 'i16': 'fptosi', 'i32': 'fptosi', 'i64': 'fptosi',
        'u8': 'fptoui', 'u16': 'fptoui', 'u32': 'fptoui', 'u64': 'fptoui',
        'f32': 'fptrunc', 'f64': None,
    }
}

numeric_cast_ops['b'] = numeric_cast_ops['i8']
