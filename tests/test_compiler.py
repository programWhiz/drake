from src.compile import compile_source


def test_add():
    program = compile_source("a = 3; b = 4; a + b")
