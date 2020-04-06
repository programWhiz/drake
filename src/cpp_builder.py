import os
import re
from pathlib import Path
from src.os_utils import run_cli_cmd
from typing import List


def compile_cpp_module(source_paths:List[str], exe_path:str):
    ret = run_cli_cmd(['g++', *source_paths, '-o', exe_path])
    assert ret == 0, "Failed to compile modules with g++."


class CPPBuilder:
    def __init__(self, c=None, h=None):
        self.c:Emitter = Emitter(c) if c else None
        self.h:Emitter = Emitter(h) if h else None

    def start(self):
        self.c.emit(f'#include \"{self.h.name}\"\n')
        h_name = re.sub(r'\W', '_', self.h.name.upper())
        self.h.emit(f'#ifndef {h_name}\n')
        self.h.emit(f'#define {h_name}\n')

    def end(self):
        self.h.emit("\n\n#endif\n")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()
        self.close()
        if exc_type:
            raise
        return self

    def close(self):
        if self.h:
            self.h.close()
        if self.c:
            self.c.close()


class WithIndenter:
    def __init__(self, emitter:"Emitter"):
        self.emitter = emitter

    def __enter__(self):
        self.emitter.indent()
        return self.emitter

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise
        self.emitter.dedent()
        return self.emitter


class Emitter:
    def __init__(self, f, name=None):
        self.name = name or os.path.basename(f)

        self.indent_count = 0
        self.indent_str = ''
        self.next_write_indents = True

        if isinstance(f, (str, Path)):
            f = open(f, 'wt')
        assert hasattr(f, 'write')
        self.fptr = f

    def with_indent(self):
        return WithIndenter(self)

    def indent(self):
        self.indent_count += 1
        self.indent_str = ' ' * self.indent_count

    def dedent(self):
        self.indent_count -= 1
        self.indent_str = ' ' * self.indent_count

    def emit(self, text):
        if self.next_write_indents or text.startswith('\n'):
            self.fptr.write(self.indent_str)
            self.next_write_indents = False

        self.fptr.write(text)
        if text.endswith('\n'):
            self.next_write_indents = True

    def close(self):
        self.fptr.close()
