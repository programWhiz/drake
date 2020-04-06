import re
from .base import test_compile_str


def test_add_ints():
    out = test_compile_str('3 + 5')
    assert out == ""
