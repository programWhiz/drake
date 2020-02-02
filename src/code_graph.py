import sys
from pathlib import Path
import antlr4
from src.exceptions import *
from src.error_listener import format_source_code_error
from src.module_search import find_module_imports, find_symbol_imports, ast_node_text
from src.grammar.DrakeParser import DrakeParser as DP


def init_code_program(ast):
    program = Program()
    # TODO: associate each module's code to a module
    program.modules['__main__'] = Module(ast)


def compile_module_cached(program, abs_name, abs_path):
    from src.compile import compile_file, get_compile_target_file

    if abs_name in program.modules:
        return program.modules[abs_name]

    if '.' in abs_name:
        parent_name = abs_name.rsplit('.', 1)[0]
        parent_path = str(Path(abs_path).parent)
        compile_module_cached(program, parent_name, parent_path)

    abs_path = get_compile_target_file(abs_path)

    module = Module(
        ast=compile_file(abs_path),
        abs_name=abs_name,
        abs_path=abs_path)

    program.modules[abs_name] = module
    module.program = program

    build_code_graph(module)

    return module


def build_code_graph(module):
    program = module.program
    imports = find_module_imports(module.ast, module.abs_name.split('.'), module.abs_path, program.search_paths)

    for im in imports:
        module.vars[im['local_name']] = compile_module_cached(
            program=program, abs_name=im['abs_name'], abs_path=im['abs_path'])

    imports = find_symbol_imports(module.ast, module.abs_name.split('.'), module.abs_path, program.search_paths)

    for im in imports:
        imported_module = compile_module_cached(program, im['module']['abs_name'], im['module']['abs_path'])
        for symbol in im['symbols']:
            try:
                module.vars[symbol['local_name']] = imported_module.vars[symbol['remote_name']]
            except KeyError:
                location_str = ast_location_str(im['module']['ast_node'])
                err = f"Module `{im['module']['abs_name']}` has no symbol `{symbol['remote_name']}` in import from {location_str}"
                sys.stderr.write(f"Symbol not found: {err}\n")
                print_source_code_error(symbol['ast_node'])
                raise SymbolNotFound(err)

    build_block(module)


def build_block(block):
    for child in block.ast_node.children:
        if isinstance(child, DP.StmtContext):
            build_graph_stmt(block, child)
        elif ast_is_eof(child):
            continue  # end of file
        else:
            raise_unknown_ast_node(block, child)


def ast_is_eof(ast_node):
    return ast_text_is(ast_node, "<EOF>")


def ast_text_is(ast_node, text):
    return isinstance(ast_node, antlr4.TerminalNode) and ast_node.symbol.text == "<EOF>"


def ast_location_str(ast_node):
    loc = ast_node_location(ast_node)
    return f"In file \"{loc['file']}\" line {loc['line']} col {loc['col']}"


def ast_node_location(ast_node):
    if isinstance(ast_node, antlr4.TerminalNode):
        loc = ast_node.symbol
    else:
        loc = ast_node.start
    return { 'file': loc.source[1].fileName, 'line': loc.line, 'col': loc.column }


def raise_unknown_ast_node(block, ast_node):
    node_type = ast_node.__class__.__name__
    if isinstance(ast_node, antlr4.TerminalNode):
        ast_text = ast_node.symbol.text
    else:
        ast_text = ast_node.start.text

    loc_str = ast_location_str(ast_node)
    error = f"{loc_str}: Unhandled AST node type: {node_type}, `{ast_text}`"
    sys.stderr.write(f"Parse error {error}\n")

    print_source_code_error(ast_node)
    raise ParseException(error)


def print_source_code_error(ast_node):
    loc = ast_node_location(ast_node)
    source_code = open(loc['file'], 'rt').read()
    source_code_error = format_source_code_error(source_code, loc['line'], loc['col'])
    sys.stderr.write(source_code_error)
    sys.stderr.write("\n")


def build_graph_stmt(block, ast_stmt):
    for child in ast_stmt.children:
        # Each statement is either simple (assign, arith, etc.) or compound (if / class / def)
        if isinstance(child, DP.Simple_stmtContext):
            build_simple_stmt(block, child)
        elif isinstance(child, DP.Compound_stmtContext):
            build_compound_stmt(block, child)
        else:
            raise_unknown_ast_node(block, child)


def build_simple_stmt(block, ast_stmt):
    """
    simple_stmt: small_stmt (';' small_stmt)* (';')? NEWLINE;
    small_stmt: (expr_stmt | del_stmt | pass_stmt | flow_stmt |
                 import_stmt | global_stmt | nonlocal_stmt | assert_stmt);
    """
    for small_stmt in ast_stmt.children:
        if isinstance(small_stmt, antlr4.TerminalNode):
            continue  # skip punctuation and spaces

        for child in small_stmt.children:
            if isinstance(child, DP.Expr_stmtContext):
                build_expr_stmt(block, child)
            elif isinstance(child, DP.Import_stmtContext):
                if isinstance(block, Module):
                    continue  # imports already handled
                else:  # handle a local import
                    build_block_local_import(block, child)
            else:
                raise_unknown_ast_node(block, child)


def build_expr_stmt(block, ast_expr):
    #  expr_stmt: anassign_stmt | augassign_stmt | assign_stmt;
    for child in ast_expr.children:
        if isinstance(child, DP.Assign_stmtContext):
            build_assign_stmt(block, child)
        else:
            raise_unknown_ast_node(block, child)


def build_assign_stmt(block, ast_node):
    left = build_test_star_stmt(block, ast_node.children[0])
    right = build_test_star_stmt(block, ast_node.children[2])
    assign = Assign(block, ast_node, left_instr=left, right_instr=right)
    # TODO: resolve the var from left and right and add edge
    block.add_instr(assign)
    return assign


def build_test_star_stmt(block, ast_node):
    # testlist_star_expr: (test | star_expr)(','(test | star_expr)) * (',')?;
    child_instrs = []
    for child in ast_node.children:
        if isinstance(child, antlr4.TerminalNode):
            continue   # skip commas in list
        elif isinstance(child, DP.TestContext):
            child_instrs.append(build_test_stmt(block, child))
        elif isinstance(child, DP.Star_exprContext):
            child_instrs.append(build_star_expr(block, child))

    if len(child_instrs) == 1:
        instr = child_instrs[0]
    else:
        instr = InstrList(block, ast_node, child_instrs)
        block.add_instr(instr)

    return instr


def build_star_expr(block, ast_node):
    expr = build_expression(block, ast_node.children[1])
    star = StarExpr(block, ast_node, expr)
    block.add_instr(star)
    return star


def build_test_stmt(block, ast_node):
    childs = ast_node.children

    # Check for a ternary statement
    if len(childs) == 5 and term_text_equals(childs[1], "if") and term_text_equals(childs[3], "else"):
        # children: <true_instr> if <cond> else <false_instr>
        true_instr = build_logical_or_test(block, childs[0])
        false_instr = build_test_stmt(block, childs[4])
        cond = build_logical_or_test(block, childs[2])
        return TernaryCond(block, ast_node, cond_instr=cond, true_instr=true_instr, false_instr=false_instr)
    elif isinstance(childs[0], DP.Or_testContext):
        return build_logical_or_test(block, childs[0])
    elif isinstance(childs[0], DP.LambdefContext):
        return build_lambda_def(block, childs[0])
    else:
        raise_unknown_ast_node(block, ast_node)


def build_logical_or_test(block, ast_node):
    instrs = []
    # or_test: and_test('or' and_test) *;
    for child in ast_node.children:
        if isinstance(child, DP.And_testContext):
            instrs.append(build_logical_and_test(block, child))

    return nest_binary_operators(block, ast_node, instrs, LogicalOr)


def build_logical_and_test(block, ast_node):
    instrs = []
    # and_test: not_test('and' not_test) *;
    for child in ast_node.children:
        if isinstance(child, DP.Not_testContext):
            instrs.append(build_logical_not_test(block, child))

    return nest_binary_operators(block, ast_node, instrs, LogicalAnd)


def build_logical_not_test(block, ast_node):
    # not_test: 'not' not_test | comparison;
    childs = ast_node.children

    if isinstance(childs[0], DP.ComparisonContext):
        return build_comparison(block, childs[0])

    # Else, is "not" followed by another not test
    nested_not = build_logical_not_test(childs[1])
    instr = LogicalNot(block=block, ast_node=ast_node, child_instr=nested_not)
    block.add_instr(instr)
    return instr


def build_comparison(block, ast_node):
    # comparison: expr (comp_op expr) *;
    child_instrs = []
    left_expr = build_expression(block, ast_node.children[0])
    operator_cls = None

    if len(ast_node.children) == 1:
        return left_expr
    # Will be multi-comparison, only chainable comparisons valid
    if len(ast_node.children) > 3:
        operator_lookup = multi_comparison_operator_classes
    # <left> <comp> <right>, all binary comparisons valid
    else:
        operator_lookup = binary_comparison_operator_classes

    for child in ast_node.children[1:]:
        if isinstance(child, DP.Comp_opsContext):
            op = ast_node_text(child)

            try:
                operator_cls = operator_lookup[op]
            except KeyError:
                raise ParseException(f"Unrecognized comparison operator {op} at {ast_location_str(child)}")
        else:
            right_expr = build_expression(block, child)
            operator_instr = operator_cls(block=block, ast_node=child, left_instr=left_expr, right_instr=right_expr)
            child_instrs.append(operator_instr)
            left_expr = right_expr

    if len(child_instrs) == 1:
        block.add_instr(child_instrs[0])
        return child_instrs[0]
    else:
        multi_comp = MultiComparison(block, ast_node, child_instrs)
        block.add_instr(multi_comp)
        return multi_comp


def nest_binary_operators(block, ast_node, instrs, op_cls):
    # If single instruction, just eval first instruction
    if len(instrs) == 1:
        return instrs[0]

    left = instrs[0]
    for right in instrs[1:]:
        left = op_cls(block=block, ast_node=ast_node, left_instr=left, right_instr=right)
        block.add_instr(left)

    return left


def build_expression(block, ast_node):
    instrs = []
    # expr: xor_expr('|' xor_expr) *;
    for child in ast_node.children:
        if isinstance(child, DP.Xor_exprContext):
            instrs.append(build_bitwise_xor_expr(block, child))

    return nest_binary_operators(block, ast_node, instrs, BitwiseOr)


def build_bitwise_xor_expr(block, ast_node):
    instrs = []
    # xor_expr: and_expr('^' and_expr) *;
    for child in ast_node.children:
        if isinstance(child, DP.And_exprContext):
            instrs.append(build_bitwise_and_expr(block, child))

    return nest_binary_operators(block, ast_node, instrs, BitwiseXOr)

def build_bitwise_and_expr(block, ast_node):
    instrs = []
    # and_expr: shift_expr('&' shift_expr) *;
    for child in ast_node.children:
        if isinstance(child, DP.Shift_exprContext):
            instrs.append(build_bitshift_expr(block, child))

    return nest_binary_operators(block, ast_node, instrs, BitwiseAnd)


def build_bitshift_expr(block, ast_node):
    left_expr = build_arith_expr(block, ast_node.children[0])
    if len(ast_node.children) == 1:
        return left_expr

    # shift_expr: arith_expr(('<<' | '>>') arith_expr) *;
    for op_node, right_node in ast_node.children[1::2]:
        right_expr = build_arith_expr(block, right_node)
        instr_class = BitShiftRight if op_node.start.text == ">>" else BitShiftLeft
        instr = instr_class(block=block, ast_node=op_node, left=left_expr, right=right_expr)
        block.add_instr(instr)
        left_expr = instr

    return left_expr

def build_arith_expr(block, ast_node):
    # arith_expr: term(('+' | '-') term) *;
    left_expr = build_term_expr(block, ast_node.children[0])
    if len(ast_node.children) == 1:
        return left_expr

    for op_node, right_node in ast_node.children[1::2]:
        right_expr = build_term_expr(block, right_node)
        op_text = ast_node_text(op_node)
        instr_class = arith_operator_classes[op_text]
        instr = instr_class(block=block, ast_node=op_node, left=left_expr, right=right_expr)
        block.add_instr(instr)
        left_expr = instr

    return left_expr


def build_term_expr(block, ast_node):
    # term: factor(('*' | '@' | '/' | '%' | '//') factor) *;
    left_expr = build_factor_expr(block, ast_node.children[0])
    if len(ast_node.children) == 1:
        return left_expr

    for op_node, right_node in ast_node.children[1::2]:
        right_expr = build_factor_expr(block, right_node)
        op_text = ast_node_text(op_node)
        instr_class = term_operator_classes[op_text]
        instr = instr_class(block=block, ast_node=op_node, left=left_expr, right=right_expr)
        block.add_instr(instr)
        left_expr = instr

    return left_expr

def build_factor_expr(block, ast_node):
    if len(ast_node.children) == 1:
        return build_power_expr(block, ast_node.children[0])

    # factor: ('+' | '-' | '~') factor | power;
    op_node, right_node = ast_node.children
    right_expr = build_factor_expr(block, right_node)
    op_text = ast_node_text(op_node)
    instr_class = factor_operator_classes[op_text]
    instr = instr_class(block=block, ast_node=op_node, child_instr=right_expr)
    block.add_instr(instr)

    return instr

def build_power_expr(block, ast_node):
    # power: atom_expr('**' factor)?;
    atom = build_atom_expr(block, ast_node.children[0])

    if len(ast_node.children) == 1:
        return atom

    factor = build_factor_expr(block, ast_node.children[2])
    op_node = ast_node.children[1]
    instr = ArithPower(block=block, ast_node=op_node, left=atom, right=factor)
    block.add_instr(instr)

    return instr


def build_atom_expr(block, ast_node):
    # first child is await?
    childs = ast_node.children
    if isinstance(childs[0], antlr4.TerminalNode):
        await_node, *childs = childs
    atom_node, *trailers = childs

    for trailer in trailers:
        raise_unknown_ast_node(block, trailer)

    return build_atom(block, atom_node)


def build_atom(block, ast_node):
    child = ast_node.children[0]
    if isinstance(child, DP.LiteralContext):
        return build_literal(block, child)
    elif isinstance(child, DP.Bare_nameContext):
        return BareName(block, child, ast_node_text(child))
    else:
        raise_unknown_ast_node(block, child)


def build_literal(block, ast_node):
    child = ast_node.children[0]
    text = child.start.text
    value, dtype = None, None

    if isinstance(child, DP.String_literalContext):
        value, dtype = text, 'str'
    elif isinstance(child, DP.Int_literalContext):
        value, dtype = int(text), 'int'
    elif isinstance(child, DP.Float_literalContext):
        value, dtype = int(text), 'float'
    elif isinstance(child, DP.Bool_literalContext):
        value, dtype = (text == "true"), 'bool'
    elif isinstance(child, DP.None_literalContext):
        value, dtype = None, 'none'
    else:
        raise_unknown_ast_node(block, ast_node)

    literal = Literal(block=block, ast_node=child.children[0], dtype=dtype, value=value)
    block.add_instr(literal)
    return literal


def build_compound_stmt(block, ast_stmt):
    # compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt;
    for child in ast_stmt.children:
        if isinstance(child, DP.If_stmtContext):
            pass
        elif isinstance(child, DP.While_stmtContext):
            pass
        elif isinstance(child, DP.For_stmtContext):
            pass
        elif isinstance(child, DP.Try_stmtContext):
            pass
        elif isinstance(child, DP.With_stmtContext):
            pass
        elif isinstance(child, DP.FuncdefContext):
            pass
        elif isinstance(child, DP.ClassdefContext):
            pass
        elif isinstance(child, DP.DecoratedContext):
            pass
        elif isinstance(child, DP.Async_stmtContext):
            pass
        else:
            raise_unknown_ast_node(block, child)


def term_text_equals(term_node, text):
    return isinstance(term_node, antlr4.TerminalNode) and term_node.symbol.text == text


class Program:
    def __init__(self):
        self.search_paths = []
        self.modules = {}


class Block:
    def __init__(self, ast=None, ast_node=None, vars=None, blocks=None, parent=None, program=None):
        self.program = program
        self.parent = parent
        self.ast = ast
        self.ast_node = ast_node
        self.vars = vars or {}
        self.blocks = blocks or []
        self.instructions = []

    def get_or_create_var(self, name, ast_node=None):
        if name in self.vars:
            return self.vars[name]
        else:
            assert ast_node, "AST Node required to create variable"
            var = Var(block=self, program=self.program, name=name, ast_node=ast_node)
            self.vars[name] = var

    def add_instr(self, instr):
        self.instructions.append(instr)

class Module(Block):
    def __init__(self, ast=None, abs_path=None, abs_name=None, vars=None, blocks=None):
        super().__init__(ast=ast, ast_node=ast, vars=vars, blocks=blocks)
        self.abs_path = abs_path
        self.abs_name = abs_name


class Func:
    def __init__(self):
        self.return_dtype = None
        self.args = None


class Var:
    """A variable handle in a block."""
    def __init__(self, name=None, block=None, program=None, ast_node=None):
        self.ast_node = ast_node
        self.name = name
        self.program = program
        self.block = block
        self.write_edges = []
        self.read_edges = []


class BareName:
    def __init__(self, block=None, ast_node=None, text=None):
        self.block = block
        self.ast_node = ast_node
        self.text = text


class Instruction():
    """An instruction in a block.  Occurs in an ordered list."""
    def __init__(self, block, ast_node):
        self.block = block
        self.ast_node = ast_node


class Literal(Instruction):
    """Any kind of literal, string, int, float."""
    def __init__(self, block, ast_node, dtype, value):
        super().__init__(block, ast_node)
        self.dtype = dtype
        self.value = value


class InstrList(Instruction):
    """
    Wraps a list of instructions such as (a, b, c, *d) for one side of an assignment
    """
    def __init__(self, block, ast_node, instrs):
        super().__init__(block, ast_node)
        self.instrs = instrs


class TernaryCond(Instruction):
    """
    A ternary conditional such as `foo() if my_bool else bar()`
    """
    def __init__(self, block, ast_node, cond_instr, true_instr, false_instr):
        super().__init__(block, ast_node)
        self.cond_instr = cond_instr
        self.true_instr = true_instr
        self.false_block = false_instr


class BinaryOp(Instruction):
    """
    Any binary operation instruction that has a left and right operand.
    """
    def __init__(self, block, ast_node, left_instr, right_instr):
        super().__init__(block, ast_node)
        self.left_instr = left_instr
        self.right_instr = right_instr


class UnaryOp(Instruction):
    """
    Any binary operation instruction that has a single operand.
    """
    def __init__(self, block, ast_node, child_instr):
        super().__init__(block, ast_node)
        self.child_instr = child_instr

class StarExpr(UnaryOp):
    pass

class Assign(BinaryOp):
    pass

class LogicalOr(BinaryOp):
    pass

class LogicalAnd(BinaryOp):
    pass

class LogicalNot(UnaryOp):
    pass

class ComparisonOp(BinaryOp):
    pass

class GreaterThanEqual(ComparisonOp):
    pass

class GreaterThan(ComparisonOp):
    pass

class LessThanEqual(ComparisonOp):
    pass

class LessThan(ComparisonOp):
    pass

class Equals(ComparisonOp):
    pass

class NotEquals(ComparisonOp):
    pass

class CompareIs(ComparisonOp):
    pass

class CompareIsNot(ComparisonOp):
    pass

class CompareIn(ComparisonOp):
    pass

class CompareNotIn(ComparisonOp):
    pass

class CompareIsA(ComparisonOp):
    pass

class MultiComparison(Instruction):
    def __init__(self, block, ast_node, comps):
        super().__init__(block, ast_node)
        self.comps = comps


multi_comparison_operator_classes = {
    ">": GreaterThan,
    "<": LessThan,
    ">=": GreaterThanEqual,
    "<=": LessThanEqual,
    "==": Equals,
}

binary_comparison_operator_classes = {
    "!=": NotEquals,
    "is": CompareIs,
    "is not": CompareIsNot,
    "in": CompareNotIn,
    "not in": CompareNotIn,
    "isa": CompareIsA,
    **multi_comparison_operator_classes
}

class BitwiseOr(BinaryOp):
    pass

class BitwiseAnd(BinaryOp):
    pass

class BitwiseXOr(BinaryOp):
    pass

class BitShiftLeft(BinaryOp):
    pass

class BitShiftRight(BinaryOp):
    pass

class ArithPlus(BinaryOp):
    pass

class ArithPower(BinaryOp):
    pass

class ArithMinus(BinaryOp):
    pass

arith_operator_classes = {
    '+': ArithPlus,
    '-': ArithMinus,
}

class ArithMultiply(BinaryOp):
    pass

class ArithDivide(BinaryOp):
    pass

class ArithModulo(BinaryOp):
    pass

class ArithIntDivide(BinaryOp):
    pass


term_operator_classes = {
    '*': ArithMultiply,
    '/': ArithDivide,
    '%': ArithModulo,
    '//': ArithIntDivide,
}

class PositiveUnary(UnaryOp):
    pass

class NegateUnary(UnaryOp):
    pass

class BitwiseNot(UnaryOp):
    pass


factor_operator_classes = {
    '+': PositiveUnary,
    '-': NegateUnary,
    '~': BitwiseNot,
}


def print_indent(str, indent):
    print("|--" * indent, str)


def print_code_tree(node, indent=0):
    for key, value in node.__dict__.items():
        if isinstance(value, (list, tuple)):
            print_indent(key, indent)
            for item in value:
                print_code_tree(value, indent + 2)

        elif isinstance(value, (str, int, float, bool)) or value is None:
            print_indent(f"{key}: {value}", indent)

        else:
            print_indent(key, indent)
            print_code_tree(value, indent + 1)

