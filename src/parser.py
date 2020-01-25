from pprint import pformat

from rply import ParserGenerator
from src.lexer import lexer

token_names = list({ rule.name for rule in lexer.rules })
token_names.extend([ "INDENT", "DEDENT" ])

precedence = [
    ('left', ['PLUS', 'DASH', 'ASTER', 'FSLASH', 'PERCENT', 'COLON', 'COMMA', 'NEWLINE']),
    ('right', ['EQ'])
]

pg = ParserGenerator(token_names, precedence=precedence)
pp = pg.production


class Node:
    def __init__(self, name, p):
        self.name = name
        self.p = p


@pp("program : stmnt_list")
@pp("program : ")
def program(p):
    return p


@pp("block : NEWLINE INDENT stmnt_list DEDENT")
def block(p):
    return Node("block", p)


@pp("stmnt_list : stmnt_list stmnt")
@pp("stmnt_list : stmnt")
def stmnt_list(p):
    return Node("stmnt_list", p)


@pp("stmnt : call NEWLINE")
@pp("stmnt : assign NEWLINE")
@pp("stmnt : serial_assign NEWLINE")
@pp("stmnt : parallel_assign NEWLINE")
@pp("stmnt : inplace NEWLINE")
@pp("stmnt : def")
@pp("stmnt : class")
@pp("stmnt : NEWLINE")
@pp("stmnt : return_expr")
@pp("stmnt : yield_expr")
@pp("stmnt : BREAK NEWLINE")
@pp("stmnt : CONTINUE NEWLINE")
def statement(p):
    return Node("stmnt", p)


@pp("yield_expr : YIELD")
@pp("yield_expr : YIELD expression")
def yield_stmnt(p):
    return Node("yield", p)


@pp("return_expr : RETURN")
@pp("return_expr : RETURN expression")
def return_stmnt(p):
    return Node("return", p)


@pp("inplace : var inplace_op expression")
def inplace(p):
    return Node("inplace", p)


@pp("inplace_op : PLUS_EQ")
@pp("inplace_op : MINUS_EQ")
@pp("inplace_op : TIMES_EQ")
@pp("inplace_op : DIV_EQ")
@pp("inplace_op : MOD_EQ")
@pp("inplace_op : DBL_AMP_EQ")
@pp("inplace_op : DBL_PIPE_EQ")
@pp("inplace_op : TILDE_EQ")
@pp("inplace_op : PIPE_EQ")
@pp("inplace_op : AMP_EQ")
def inplace_op(p):
    return Node("inplace_op", p)


@pp("binary_op : PLUS")
@pp("binary_op : DASH")
@pp("binary_op : LT")
@pp("binary_op : GT")
@pp("binary_op : LE")
@pp("binary_op : GE")
@pp("binary_op : EQ")
@pp("binary_op : DBL_EQ")
@pp("binary_op : ASTER")
@pp("binary_op : FSLASH")
@pp("binary_op : PERCENT")
@pp("binary_op : AMP")
@pp("binary_op : PIPE")
@pp("binary_op : TILDE")
@pp("binary_op : AND")
@pp("binary_op : OR")
def binary_op(p):
    return Node("binary_op", p)


@pp("unary_op : DASH")
@pp("unary_op : NOT")
@pp("unary_op : TILDE")
def unary_op(p):
    return Node("unary_op", p)


@pp("var : WORD")
@pp("var : WORD DOT var")
def var(p):
    return Node("var", p)


@pp('assign : expression EQ expression')
def assign_op(p):
    return Node("assign", p)


@pp('parallel_assign : parallel_assign_vars EQ expression')
def multi_assign_op(p):
    return Node("parallel_assign", p)


@pp('parallel_assign_vars : parallel_assign_vars COMMA var')
@pp('parallel_assign_vars : var')
def parallel_assign_vars(p):
    return Node("parallel_assign_vars", p)


@pp('serial_assign : serial_assign COMMA assign')
@pp('serial_assign : assign')
def serial_assign(p):
    return Node("serial_assign", p)


@pp('call : expression OPEN_PAREN call_args CLOSE_PAREN')
def func_call(p):
    return Node("call", p)


@pp('call_args : ')
@pp('call_args : expression')
@pp('call_args : expression COMMA call_args')
def call_args(p):
    return Node("call_args", p)


@pp('expression : unary_op expression')
@pp('expression : expression binary_op expression')
@pp('expression : literal')
@pp('expression : var')
def expression(p):
    return Node("expr", p)


@pp('expression : OPEN_PAREN expression CLOSE_PAREN')
def paren_expr(p):
    return Node("expr", p[1])


@pp('int : INTEGER')
def integer(p):
    return Node("int", p)


@pp('float : FLOAT')
def integer(p):
    return Node("float", p)


@pp("str : STR_SINGLE_SINGLE")
@pp("str : STR_SINGLE_DOUBLE")
@pp("str : STR_TRIPLE_SINGLE")
@pp("str : STR_TRIPLE_DOUBLE")
def string(p):
    return Node("string", p)


@pp('literal : int')
@pp('literal : float')
@pp('literal : str')
def literal(p):
    return Node("literal", p)


@pp('def : DEF WORD OPEN_PAREN def_args CLOSE_PAREN COLON block')
def def_func(p):
    return Node("def", p)


@pp('def_args : ')
@pp('def_args : def_args COMMA def_arg')
@pp('def_args : def_arg')
def def_args(p):
    return Node("def_args", p)


@pp('def_arg : WORD')
@pp('def_arg : WORD EQ expression')
def def_arg(p):
    return Node("def_arg", p)


@pp('class : CLASS WORD class_inherit COLON block')
def def_class(p):
    return Node("class", p)


@pp('class_inherit : ')
@pp('class_inherit : OPEN_PAREN CLOSE_PAREN')
@pp('class_inherit : OPEN_PAREN class_list CLOSE_PAREN')
def class_inherit(p):
    return Node("class_inherit", p)


@pp("class_list : class_list COMMA var")
@pp("class_list : var")
def class_list(p):
    return Node("class_list", p)


parser = pg.build()
