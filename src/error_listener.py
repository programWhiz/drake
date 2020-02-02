import sys
from antlr4.error.ErrorListener import ErrorListener
from src.exceptions import *


class DrakeErrorListener(ErrorListener):
    def __init__(self, file_path:str):
        self.file_path = file_path

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_msg = f"Syntax error in {self.file_path} at line {line} col {column}: {msg}"
        sys.stderr.write(error_msg)
        sys.stderr.write("\n")
        source_code = open(self.file_path, 'r').read()
        source_code_error = format_source_code_error(source_code, line, column)
        sys.stderr.write(source_code_error)
        sys.stderr.write("\n")

        raise ParseException(error_msg)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise ParseException(f"Ambiguous syntax in {self.file_path} at line {line} col {column}: {msg}")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise ParseException(f"Syntax error in {self.file_path} at line {line} col {column}: {msg}")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise ParseException(f"Syntax error in {self.file_path} at line {line} col {column}: {msg}")


def format_source_code_error(source:str, lineno:int, colno:int, scope:int=4):
    error_msg = ""
    lines = source.split('\n')
    start_line = max(lineno - scope, 0)
    end_line = min(lineno + scope + 1, len(lines))
    arrow_marker, empty_marker = ">>> ", "    "
    for i in range(start_line, end_line):
        line = lines[i]
        line_no_prefix = f"{i}.\t"

        if i == lineno - 1:
            error_msg += f"{arrow_marker}{line_no_prefix}{line}"
            num_spaces = len(arrow_marker) + len(line_no_prefix) + colno
            spaces = " " * num_spaces
            error_msg += f"\n{spaces}^"
        else:
            error_msg += f"{empty_marker}{line_no_prefix}{line}"

        error_msg += "\n"

    return error_msg