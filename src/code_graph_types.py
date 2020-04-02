import antlr4


class CodeNode:
    def calc_types(self):
        pass


class Program(CodeNode):
    def __init__(self):
        self.build_dir = ""
        self.search_paths = []
        self.modules = { }

    def calc_types(self):
        for module in self.modules.values():
            module.calc_types()


class Block(CodeNode):
    def __init__(self, ast=None, ast_node=None, local_vars=None,
                 global_vars=None, blocks=None, parent=None, program=None):
        self.program = program
        self.parent = parent
        self.ast = ast
        self.ast_node = ast_node
        self.local_vars = local_vars or { }
        self.global_vars = global_vars or { }
        self.blocks = blocks or []
        self.instructions = []

    def add_instr(self, instr):
        self.instructions.append(instr)

        if isinstance(instr, Block):
            self.blocks.append(instr)
            instr.parent = self

    def calc_types(self):
        for instr in self.instructions:
            instr.calc_type()


class Module(Block):
    def __init__(self, *args, abs_path=None, abs_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.abs_path = abs_path
        self.abs_name = abs_name


class FuncDef(Block):
    def __init__(self, *args, name=None, params=None, returns=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.params = params
        self.returns = returns


class Var(CodeNode):
    """A variable handle in a block."""

    def __init__(self, name=None, block=None, program=None, ast_node=None):
        self.ast_node = ast_node
        self.name = name
        self.program = program
        self.block = block
        self.write_edges = []
        self.read_edges = []


class BareName(CodeNode):
    def __init__(self, block=None, ast_node=None, text=None):
        self.block = block
        self.ast_node = ast_node
        self.text = text


class Instruction(CodeNode):
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
        self.instrs = instrs or []

    def add_instr(self, instr):
        self.instrs.append(instr)


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


class CollapseStarExpr(UnaryOp):
    pass


class ExpandStarExpr(UnaryOp):
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


class ArithMultiply(BinaryOp):
    pass


class ArithDivide(BinaryOp):
    pass


class ArithModulo(BinaryOp):
    pass


class ArithIntDivide(BinaryOp):
    pass


class PositiveUnary(UnaryOp):
    pass


class NegateUnary(UnaryOp):
    pass


class BitwiseNot(UnaryOp):
    pass


class FuncCall(Instruction):
    def __init__(self, block, ast_node, func_ptr_instr, args=None):
        super().__init__(block, ast_node)
        self.func_ptr_instr = func_ptr_instr
        self.args = args


class ListGenerator(Block):
    pass


class DotOperator(BinaryOp):
    pass


class KeyWordArg(BinaryOp):
    pass


class KeyWordArgVar(UnaryOp):
    pass


class ArgListVar(UnaryOp):
    pass


class KeyValueExpand(UnaryOp):
    pass


class GetItem(BinaryOp):
    pass


class SubscriptList(InstrList):
    pass


class SliceOp(Instruction):
    def __init__(self, block, ast_node, start, stop, stride):
        super().__init__(block, ast_node)
        self.start = start
        self.stop = stop
        self.stride = stride


class KeyValuePair(BinaryOp):
    pass


class KeyValueList(InstrList):
    pass


class DictComprehension(Instruction):
    def __init__(self, block, ast_node, kvp_instr=None, for_loop=None):
        super().__init__(block, ast_node)
        self.kvp_instr = kvp_instr
        self.for_loop = for_loop


class SetComprehension(Instruction):
    def __init__(self, block, ast_node, item_instr=None, for_loop=None):
        super().__init__(block, ast_node)
        self.item_instr = item_instr
        self.for_loop = for_loop


class ListComprehension(SetComprehension):
    pass


class ForLoop(Block):
    def __init__(self, *args, iter_vars=None, iter_src=None, filter_cond=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.iter_vars = iter_vars
        self.iter_src = iter_src
        self.filter_cond = filter_cond


class ClassDef(Block):
    def __init__(self, *args, class_name=None, body=None, supers=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_name = class_name
        self.body = body
        self.supers = supers


class NamedFuncArg(Instruction):
    def __init__(self, block, ast_node, name:str, default_value=None, type_qual=None):
        super().__init__(block, ast_node)
        self.name = name
        self.default_value = default_value
        self.type_qual = type_qual


class TypeQualifier(Instruction):
    def __init__(self, block, ast_node, type_name:str, template_def:"TemplateDef"):
        super().__init__(block, ast_node)
        self.type_name = type_name
        self.template_def = template_def


class TemplateDef(Instruction):
    def __init__(self, block, ast_node, args):
        super().__init__(block, ast_node)
        self.args = args


class StarFuncArg(Instruction):
    def __init__(self, block, ast_node, name, type_qual):
        super().__init__(block, ast_node)
        self.name = name
        self.type_qual = type_qual


class StarKwFuncArg(Instruction):
    def __init__(self, block, ast_node, name, type_qual):
        super().__init__(block, ast_node)
        self.name = name
        self.type_qual = type_qual


class WhileLoop(Block):
    def __init__(self, *args, cond, **kwargs):
        super().__init__(*args, **kwargs)
        self.cond = cond


class DoWhileLoop(Block):
    def __init__(self, *args, cond, **kwargs):
        super().__init__(*args, **kwargs)
        self.cond = cond


class IfCondition(Block):
    def __init__(self, *args, cond=None, elif_blocks=None, else_block=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cond = cond
        self.elif_blocks = elif_blocks or []
        self.else_block = else_block

    def add_elif(self, instr):
        self.elif_blocks.append(instr)

    def calc_types(self):
        super().calc_types()
        self.cond.calc_types()
        for block in self.elif_blocks:
            block.calc_types()
        if self.else_block:
            self.else_block.calc_types()


class ElifCondition(Block):
    def __init__(self, *args, cond=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cond = cond

    def calc_types(self):
        super().calc_types()
        self.cond.calc_types()


class ElseBlock(Block):
    pass


class Yield(Instruction):
    def __init__(self, block, ast_node, expr=None):
        super().__init__(block, ast_node)
        self.expr = None

    def calc_types(self):
        if self.expr:
            self.expr.calc_types()


class Return(Instruction):
    def __init__(self, block, ast_node, expr=None):
        super().__init__(block, ast_node)
        self.expr = None

    def calc_types(self):
        if self.expr:
            self.expr.calc_types()


class Raise(Instruction):
    def __init__(self, block, ast_node, expr=None, from_expr=None):
        super().__init__(block, ast_node)
        self.expr = None
        self.from_expr = from_expr

    def calc_types(self):
        super().calc_types()


class Break(Instruction):
    pass


class Continue(Instruction):
    pass


def print_indent(str, indent):
    print("|--" * indent, str)


def print_code_tree(node, indent=0, prefix="", visited=None):
    print_indent(f"{prefix}{node.__class__.__name__}", indent)

    if visited is None:
        visited = set()
    if node in visited:
        return
    visited.add(node)

    indent += 1

    for key, value in node.__dict__.items():
        if isinstance(value, (list, tuple)):
            print_indent(f"{key} [List]", indent)
            for i, item in enumerate(value):
                if isinstance(item, CodeNode):
                    print_code_tree(item, indent + 1, f"{i}. ", visited)
                else:
                    print_indent(f"{i}. {item}", indent + 1)

        elif isinstance(value, CodeNode):
            print_code_tree(value, indent, f"{key}: ", visited)

        elif isinstance(value, antlr4.ParserRuleContext):
            print_indent(f"{key}: {value.start.text}", indent)

        else:
            print_indent(f"{key}: {value}", indent)


term_operator_classes = {
    '*': ArithMultiply,
    '/': ArithDivide,
    '%': ArithModulo,
    '//': ArithIntDivide,
}

arith_operator_classes = {
    '+': ArithPlus,
    '-': ArithMinus,
}

factor_operator_classes = {
    '+': PositiveUnary,
    '-': NegateUnary,
    '~': BitwiseNot,
}

math_operator_classes = {
    **arith_operator_classes,
    **term_operator_classes,
    '<<': BitShiftLeft,
    '>>': BitShiftRight,
    '|': BitwiseOr,
    '&': BitwiseAnd,
    '^': BitwiseXOr,
    '**': ArithPower,
}

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
