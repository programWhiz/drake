from typing import List


class Node:
    def __init__(self, name, token):
        self.name = name
        self.token = token


class StmntList(Node):
    def __init__(self, stmnts):
        super().__init__("stmnt_list", None)
        self.stmnts = stmnts


class BreakStmnt(Node):
    pass


class ContinueStmnt(Node):
    pass


class StringLiteral(Node):
    def __init__(self, token, value="", is_multiline=False, is_format=False, is_regex=False):
        super().__init__("string", token)
        self.value = value
        self.is_multiline = is_multiline
        self.is_format = is_format
        self.is_regex = is_regex


class IntLiteral(Node):
    def __init__(self, token, value:int):
        super().__init__("int", token)
        self.value = value


class FloatLiteral(Node):
    def __init__(self, token, value:float):
        super().__init__("float", token)
        self.value = value


class ReturnStmnt(Node):
    def __init__(self, token, return_expr):
        super().__init__("return", token)
        self.return_expr = return_expr


class PassStmnt(Node):
    def __init__(self, token):
        super().__init__("pass", token)


class YieldStmnt(Node):
    def __init__(self, token, yield_expr):
        super().__init__("yield", token)
        self.yield_expr = yield_expr


class BinaryOp(Node):
    def __init__(self, name, token):
        super().__init__(name, token)
        self.left_op = None
        self.right_op = None


class FuncDef(Node):
    def __init__(self, name, token, args, body):
        super().__init__(name, token)
        self.args = args
        self.body = body


class FuncArg(Node):
    pass


class FuncCall(Node):
    def __init__(self, token, func, args):
        super().__init__("call", token)
        self.func = func
        self.args = args


class AssignStmnt(Node):
    def __init__(self, assign_vars, source_expr):
        # super().__init__("assign", assign_vars[0].token)
        super().__init__("assign", None)
        self.assign_vars = assign_vars
        self.source_expr = source_expr


class VarNode(Node):
    def __init__(self, name, token):
        super().__init__(name, token)
        self.name_dot_list = [ name ]
        self.name_tokens = [ token ]

    def add_name(self, name, token):
        if not name.startswith("."):
            self.name += "."
        self.name += name
        self.name_dot_list.append(name)
        self.name_tokens.append(token)


class ModuleNode(VarNode):
    def __init__(self, name, token):
        super().__init__(name, token)
        self.abs_name = None
        self.abs_path = None


class InPlace(Node):
    def __init__(self, lhs, op, rhs):
        super().__init__(op.name, op)
        self.lhs = lhs
        self.op = op
        self.rhs = rhs


class ClassDef(Node):
    def __init__(self, name, token, inherit, block):
        super().__init__(name, token)
        self.inherit = inherit
        self.block = block


class ClassRef(Node):
    pass


class IfNode(Node):
    def __init__(self, token, cond, body, elif_nodes, else_node):
        super().__init__("if", token)
        self.cond = cond
        self.body = body
        self.elif_nodes = elif_nodes
        self.else_node = else_node


class ElifNode(Node):
    def __init__(self, token, cond, body):
        super().__init__("elif", token)
        self.cond = cond
        self.body = body


class ElseNode(Node):
    def __init__(self, token, body):
        super().__init__("else", token)
        self.body = body


class ImportStmnt(Node):
    def __init__(self, token, module, symbols=None, import_all=False):
        super().__init__(module.name, token)
        self.module:ModuleNode = module
        self.symbols:List[VarNode] = symbols or []
        self.import_all:bool = import_all


def print_indented(indent, text):
    print("  " * indent, text)


def print_ast_debug(node, indent=0):
    symbol = getattr(node, 'start', getattr(node, 'symbol', None))
    print_indented(indent, f"{node.__class__.__name__} : {symbol}")
    if hasattr(node, 'children'):
        for child in node.children:
            print_ast_debug(child, indent + 1)


def surf_ast(node, path):
    parts = path.split('/')

    if isinstance(node, (list, tuple)):
        nodes = node
    else:
        nodes = [ node ]

    for part in parts:
        nodes = [ child for node in nodes for child in node.children if child.__class__.__name__ == part ]

    return nodes
