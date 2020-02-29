import sys
from io import StringIO
from src.exceptions import BuildException
from src.warnings import Warnings


def test_warning():
    stderr = StringIO()
    sys.stderr = stderr

    Warnings.duplicate_var.level = Warnings.WARNING
    Warnings.emit(Warnings.duplicate_var, "Testing this")

    assert str(stderr)


def test_error():
    stderr = StringIO()
    sys.stderr = stderr

    Warnings.duplicate_var.level = Warnings.ERROR

    try:
        Warnings.emit(Warnings.duplicate_var, "Testing this")
        assert False, 'Expected ERROR to throw BuildException'
    except BuildException:
        pass

    assert str(stderr)
