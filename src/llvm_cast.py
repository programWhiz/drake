from llvmlite import ir as ll

llvm_type_shortname = {
    'half': 'f16', 'float': 'f32', 'double': 'f64',
}

llvm_float_types = (ll.FloatType, ll.HalfType, ll.DoubleType)


def noop(bb: ll.IRBuilder, val):
    return val


def sext(bits):  # signed integer extend
    def wrap(bb: ll.IRBuilder, val):
        return bb.sext(val, ll.IntType(bits))

    return wrap


def zext(bits):   # unsigned integer ext
    def wrap(bb: ll.IRBuilder, val):
        return bb.zext(val, ll.IntType(bits))

    return wrap


def trunc(bits):
    def wrap(bb: ll.IRBuilder, val):
        return bb.trunc(val, ll.IntType(bits))

    return wrap


def fpext(bits):
    def wrap(bb: ll.IRBuilder, val):
        return bb.fpext(val, ftype(bits))

    return wrap


def ftype(bits):
    return ll.FloatType() if bits < 64 else ll.DoubleType()


def fptrunc(bits):
    def wrap(bb: ll.IRBuilder, val):
        return bb.fptrunc(val, ftype(bits))

    return wrap


def fptosi(bits):
    def wrap(bb: ll.IRBuilder, val):
        return bb.fptosi(val, ll.IntType(bits))

    return wrap


def fptoui(bits):
    def wrap(bb: ll.IRBuilder, val):
        return bb.fptoui(val, ll.IntType(bits))

    return wrap


def sitofp(bits):
    def wrap(bb: ll.IRBuilder, val):
        return bb.sitofp(val, ftype(bits))

    return wrap


def uitofp(bits):
    def wrap(bb: ll.IRBuilder, val):
        return bb.uitofp(val, ftype(bits))

    return wrap


cast_types = {
    'int8': {
        'int8': noop, 'int16': sext(16), 'int32': sext(32), 'int64': sext(64),
        'uint8': noop, 'uint16': zext(16), 'uint32': zext(32), 'uint64': zext(64),
        'float32': sitofp(32), 'float64': sitofp(64),
    },
    'int16': {
        'int8': trunc(8), 'int16': noop, 'int32': sext(32), 'int64': sext(64),
        'uint8': trunc(8), 'uint16': noop, 'uint32': zext(32), 'uint64': zext(64),
        'float32': sitofp(32), 'float64': sitofp(64),
    },
    'int32': {
        'int8': trunc(8), 'int16': trunc(16), 'int32': noop, 'int64': sext(64),
        'uint8': trunc(8), 'uint16': trunc(16), 'uint32': noop, 'uint64': zext(64),
        'float32': sitofp(32), 'float64': sitofp(64),
    },
    'int64': {
        'int8': trunc(8), 'int16': trunc(16), 'int32': trunc(32), 'int64': noop,
        'uint8': trunc(8), 'uint16': trunc(16), 'uint32': trunc(32), 'uint64': noop,
        'float32': sitofp(32), 'float64': sitofp(64),
    },
    'float32': {
        'int8': fptosi(8), 'int16': fptosi(16), 'int32': fptosi(32), 'int64': fptosi(64),
        'uint8': fptoui(8), 'uint16': fptoui(16), 'uint32': fptoui(32), 'uint64': fptoui(64),
        'float32': noop, 'float64': fpext(64),
    },
    'float64': {
        'int8': fptosi(8), 'int16': fptosi(16), 'int32': fptosi(32), 'int64': fptosi(64),
        'uint8': fptoui(8), 'uint16': fptoui(16), 'uint32': fptoui(32), 'uint64': fptoui(64),
        'float32': fptrunc(32), 'float64': noop,
    }
}

cast_types['bool'] = cast_types['int8']
cast_types['int'] = cast_types['int32']
cast_types['float'] = cast_types['float32']
