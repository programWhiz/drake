from pprint import pformat

from rply import ParserGenerator
from src.lexer import lexer
from src.drake_ast import *

token_names = list({ rule.name for rule in lexer.rules })
token_names.extend(["INDENT", "DEDENT"])

precedence = [
    ('left', ['PLUS', 'DASH', 'ASTER', 'FSLASH', 'PERCENT', 'COLON', 'COMMA', 'NEWLINE']),
    ('right', ['EQ'])
]

pg = ParserGenerator(token_names, precedence=precedence)
pp = pg.production


@pp("program : stmnt_list")
@pp("program : ")
def program(p):
    return p


@pp("block : NEWLINE INDENT stmnt_list DEDENT")
def block(p):
    return p[2]


@pp("stmnt_list : stmnt_list stmnt")
@pp("stmnt_list : stmnt")
def stmnt_list(p):
    if len(p) == 1:
        return p
    else:
        p[0].append(p[1])
        return p[0]


@pp("stmnt : expression NEWLINE")
@pp("stmnt : assign NEWLINE")
@pp("stmnt : serial_assign NEWLINE")
@pp("stmnt : parallel_assign NEWLINE")
@pp("stmnt : inplace NEWLINE")
@pp("stmnt : class")
@pp("stmnt : def")
def statement(p):
    return p[0]


@pp("stmnt : NEWLINE")
@pp("stmnt : PASS NEWLINE")
def stmnt_empty(p):
    return PassStmnt(p[0])


@pp("stmnt : CONTINUE NEWLINE")
def continue_stmnt(p):
    return ContinueStmnt(p[0])


@pp("stmnt : BREAK NEWLINE")
def break_stmnt(p):
    return BreakStmnt(p[0])


@pp("stmnt : YIELD NEWLINE")
@pp("stmnt : YIELD expression NEWLINE")
def yield_stmnt(p):
    expr = None if len(p) < 3 else p[1]
    return YieldStmnt(p[0], expr)


@pp("stmnt : RETURN NEWLINE")
@pp("stmnt : RETURN expression NEWLINE")
def return_stmnt(p):
    expr = None if len(p) < 3 else p[1]
    return ReturnStmnt(p[0], expr)


@pp("inplace : var inplace_op expression")
def inplace(p):
    return InPlace(op=p[1], var=p[0], expr=p[2])


@pp("inplace_op : PLUS_EQ")
@pp("inplace_op : MINUS_EQ")
@pp("inplace_op : TIMES_EQ")
@pp("inplace_op : DIV_EQ")
@pp("inplace_op : DBL_DIV_EQ")
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
@pp("binary_op : DBL_FSLASH")
@pp("binary_op : PERCENT")
@pp("binary_op : AMP")
@pp("binary_op : PIPE")
@pp("binary_op : TILDE")
@pp("binary_op : AND")
@pp("binary_op : OR")
def binary_op(p):
    return BinaryOp(p[0].value, p[0])


@pp("unary_op : DASH")
@pp("unary_op : NOT")
@pp("unary_op : TILDE")
def unary_op(p):
    return Node("unary_op", p)


@pp("var : WORD")
@pp("var : var DOT WORD")
def var(p):
    if len(p) == 1:
        return VarNode(p[0].value, p[0])
    else:
        p[0].add_name(p[2].value, p[2])
        return p[0]


@pp('assign : expression EQ expression')
def assign_op(p):
    return Node("assign", p)


@pp('parallel_assign : parallel_assign_vars EQ expression')
def multi_assign_op(p):
    return AssignStmnt(p[0], p[2])


@pp('parallel_assign_vars : parallel_assign_vars COMMA var')
@pp('parallel_assign_vars : var')
def parallel_assign_vars(p):
    if len(p) == 1:
        return p
    else:
        p[0].append(p[2])
        return p[0]


@pp('serial_assign : serial_assign COMMA assign')
@pp('serial_assign : assign')
def serial_assign(p):
    return Node("serial_assign", p)


@pp('expression : expression OPEN_PAREN call_args CLOSE_PAREN')
def func_call(p):
    return FuncCall(token=p[1], func=p[0], args=p[2])


@pp('call_args : ')
@pp('call_args : expression')
@pp('call_args : call_args COMMA expression')
def call_args(p):
    if len(p) == 0:
        return []
    if len(p) == 1:
        return p
    else:  # append list
        p[0].append(p[2])
        return p[0]


@pp('expression : expression binary_op expression')
def binary_expr(p):
    p[1].left_op = p[0]
    p[1].right_op = p[2]
    return p[1]


@pp('expression : unary_op expression')
def unary_expr(p):
    p[0].operand = p[1]
    return p[0]


@pp('expression : literal')
@pp('expression : var')
def expression(p):
    return p[0]


@pp('expression : OPEN_PAREN expression CLOSE_PAREN')
def paren_expr(p):
    return p[1]


@pp('int : INTEGER')
@pp('int : DEC_INT')
@pp('int : BIN_INT')
@pp('int : HEX_INT')
@pp('int : OCT_INT')
def integer(p):
    return IntLiteral(p[0], int(p[0].value))


@pp('float : FLOAT')
def integer(p):
    return FloatLiteral(p[0], float(p[0].value))


@pp("str : STR_SINGLE_SINGLE")
@pp("str : STR_SINGLE_DOUBLE")
@pp("str : STR_TRIPLE_SINGLE")
@pp("str : STR_TRIPLE_DOUBLE")
def string(p):
    name = p[0].name
    s = p[0].value

    node = StringLiteral(p[0])
    node.is_regex = s[0] == 'r'
    node.is_format = s[0] == 'f'

    if node.is_regex or node.is_format:
        s = s[1:]

    node.is_multiline = "TRIPLE" in name

    if node.is_multiline:  # trim triple quote chars
        node.value = s[3:-3]

    else:  # trim single quote chars
        node.value = s[1:-1]

    return node


@pp('literal : int')
@pp('literal : float')
@pp('literal : str')
def literal(p):
    return p[0]


@pp('def : DEF WORD OPEN_PAREN def_args CLOSE_PAREN COLON block')
def def_func(p):
    return FuncDef(name=p[1].value, token=p[1], args=p[3], block=p[-1])


@pp('def_args : ')
@pp('def_args : def_args COMMA def_arg')
@pp('def_args : def_arg')
def def_args(p):
    if len(p) == 0:  # no args
        return []
    if len(p) == 1:  # single arg
        return p
    else:  # append comma separated args
        p[0].append(p[2])
        return p[0]


@pp('def_arg : WORD')
@pp('def_arg : WORD EQ expression')
def def_arg(p):
    arg = FuncArg(name=p[0].value, token=p[0])

    if len(p) > 1:
        raise NotImplementedError("TODO: handle keyword/default function args")

    return arg


@pp('class : CLASS WORD class_inherit COLON block')
def def_class(p):
    return ClassDef(p[1].value, p[1], p[2], p[4])


@pp('class_inherit : ')
@pp('class_inherit : OPEN_PAREN class_list CLOSE_PAREN')
def class_inherit(p):
    if len(p) == 0:
        return []
    else:
        return p[1]


@pp("class_list : class_list COMMA var")
@pp("class_list : var")
@pp("class_list : ")
def class_list(p):
    if len(p) == 0:  # no classes
        return p
    elif len(p) == 1:  # single class
        return p
    else:  # multiple items
        p[0].append(p[2])
        return p[0]


@pp("stmnt : IF expression COLON block elif_stmnt else_stmnt")
def if_block(p):
    return IfNode(token=p[0], cond=p[1], body=p[3], elif_nodes=p[4], else_node=p[5])


@pp("else_stmnt : ELSE COLON block")
def else_block(p):
    return ElseNode(token=p[0], body=p[2])


@pp("else_stmnt : ")
def empty_else_block(p):
    return None


@pp("elif_stmnt : ")
def empty_elif(p):
    return []


@pp("elif_stmnt : ELIF expression COLON block")
def elif_block(p):
    return ElifNode(token=p[0], cond=p[1], body=p[3])


@pp("elif_stmnt : elif_stmnt ELIF expression COLON block")
def elif_block(p):
    p[0].append(ElifNode(token=p[1], cond=p[2], body=p[4]))
    return p[0]


parser = pg.build()
