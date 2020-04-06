import re
from .base import test_compile_str


def test_newline():
    out = test_compile_str('print()')
    assert out == ""


def test_hello_world():
    out = test_compile_str('print("Hello world 世界!")')
    assert out == "Hello world 世界!"


def test_print_int():
    out = test_compile_str('print(3)')
    assert out == "3"


def test_print_float():
    out = test_compile_str('print(3.141519)')
    assert re.match(r"3.1415\d+", out)


def test_print_bool():
    out = test_compile_str('print(true)')
    assert out == "true"


def test_print_multi():
    out = test_compile_str(' print(32, 2.0, true, "Goodbye Cruel World") ')
    assert re.match(r"^32 2.00+ true Goodbye Cruel World$", out)
