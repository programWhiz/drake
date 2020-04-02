import sys
from src.exceptions import *


class WarningType:
    def __init__(self, name, level):
        self.name = name
        self.level = level


class _Warnings:
    ERROR = 2
    WARNING = 1
    IGNORE = 0

    shadow_var = WarningType('shadow_var', WARNING)
    change_var_type = WarningType('change_var_type', WARNING)
    duplicate_var = WarningType('duplicate_var', ERROR)
    implicit_cast_int_signed_unsigned = WarningType('implicit_cast_int_signed_unsigned', ERROR)
    implicit_cast_int_more_precision = WarningType('implicit_cast_float_more_precision', WARNING)
    implicit_cast_int_less_precision = WarningType('implicit_cast_float_less_precision', WARNING)
    implicit_cast_int_float = WarningType('implicit_cast_int_float', ERROR)
    implicit_cast_float_int = WarningType('implicit_cast_int_float', ERROR)
    implicit_cast_float_more_precision = WarningType('implicit_cast_float_more_precision', WARNING)
    implicit_cast_float_less_precision = WarningType('implicit_cast_float_less_precision', WARNING)

    def emit(self, err, msg):
        if err.level <= self.IGNORE:
            return

        err_msg = f"Build error {err.name}: {msg}"

        if err.level >= self.ERROR:
            print("[ERROR]", err_msg, file=sys.stderr)
            raise BuildException(err_msg)

        elif err.level >= self.WARNING:
            print("[WARNING]", err_msg, file=sys.stderr)


Warnings = _Warnings()
