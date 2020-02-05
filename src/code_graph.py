import sys
from pathlib import Path
import antlr4
from src.exceptions import *
from src.error_listener import format_source_code_error
from src.module_search import find_module_imports, find_symbol_imports, ast_node_text
from src.grammar.DrakeParser import DrakeParser as DP
from src.code_graph_types import *


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

    print("==== Printing code tree for module: ", module.abs_name, "====")
    print_code_tree(module)
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

    print_code_tree(module)


def build_block(block):
    for child in block.ast_node.children:
        if isinstance(child, DP.StmtContext):
            build_statement(block, child)
        elif ast_is_empty(child):
            continue  # end of file
        else:
            raise_unknown_ast_node(block, child)


def ast_is_empty(ast_node):
    return ast_text_is(ast_node, ("<EOF>", "\n"))


def ast_text_is(ast_node, text):
    if not isinstance(text, (tuple, list)):
        text = (text,)
    return isinstance(ast_node, antlr4.TerminalNode) and ast_node.symbol.text in text


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


def build_statement(block, ast_stmt):
    child = ast_stmt.children[0]
    # stmt: simple_stmt | compound_stmt;
    if isinstance(child, DP.Simple_stmtContext):
        return build_simple_stmt(block, child)
    else:
        return build_compound_stmt(block, child)


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
            elif isinstance(child, DP.Pass_stmtContext):
                continue  # skip instruction
            elif isinstance(child, DP.Flow_stmtContext):
                build_flow_statement(block, child)
            else:
                raise_unknown_ast_node(block, child)


def build_flow_statement(block, ast_node):
    """
    flow_stmt: break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt;
    """
    node = ast_node.children[0]
    if isinstance(node, DP.Break_stmtContext):
        instr = Break(block, node)
        block.add_instr(instr)
    elif isinstance(node, DP.Continue_stmtContext):
        instr = Continue(block, node)
        block.add_instr(instr)
    elif isinstance(node, DP.Yield_stmtContext):
        instr = build_yield_stmt(block, node)
    elif isinstance(node, DP.Raise_stmtContext):
        instr = build_raise_stmt(block, node)
    elif isinstance(node, DP.Return_stmtContext):
        instr = build_return_stmt(block, node)
    else:
        raise_unknown_ast_node(block, node)

    return instr


def build_return_stmt(block, ast_node):
    # return_stmt: 'return' (testlist)?;
    instr = Return(block, ast_node)
    if len(ast_node.children) > 1:
        instr.expr = build_test_list(block, ast_node.children[1])
    block.add_instr(instr)
    return instr


def build_raise_stmt(block, ast_node):
    # raise_stmt: 'raise' (test ('from' test)?)?;
    instr = Raise(block, ast_node)
    block.add_instr(instr)

    childs = ast_node.children

    if len(childs) >= 2:  # raise e
        instr.expr = build_test_stmt(block, childs[1])

    if len(childs) >= 3:  # raise ParseException from e
        instr.from_expr = build_test_stmt(block, childs[3])

    return instr


def build_yield_stmt(block, ast_node):
    # yield_stmt : yield_expr ;
    return build_yield_expr(block, ast_node.children[0])


def build_yield_expr(block, ast_node):
    # yield_expr: 'yield' (yield_arg)?;
    instr = Yield(block=block, ast_node=ast_node)
    block.add_instr(instr)

    if len(ast_node.children) >= 2:
        instr.expr = build_yield_arg(block, ast_node.children[1])

    return instr


def build_yield_arg(block, ast_node):
    # yield_arg: 'from' test | testlist;
    if len(ast_node.children) == 1:  # yield <x>
        return build_test_list(block, ast_node.children[0])
    else:  # yield from <x>
        return build_test_stmt(block, ast_node.children[1])


def build_expr_stmt(block, ast_expr):
    #  expr_stmt: anassign_stmt | augassign_stmt | assign_stmt;
    for child in ast_expr.children:
        if isinstance(child, DP.Assign_stmtContext):
            build_assign_stmt(block, child)
        elif isinstance(child, DP.Augassign_stmtContext):
            build_aug_assign_stmt(block, child)
        elif isinstance(child, DP.Anassign_stmtContext):
            build_anassign_stmt(block, child)
        else:
            raise_unknown_ast_node(block, child)


def build_aug_assign_stmt(block, ast_node):
    # augassign_stmt: testlist_star_expr augassign (yield_expr | testlist);
    # augassign: ('+=' | '-=' | '*=' | '@=' | '/=' | '%=' | '&=' | '|=' | '^=' | '<<=' | '>>=' | '**=' | '//=');

    left_instr = build_test_star_stmt(block, ast_node.children[0])
    aug_node = ast_node.children[1]

    if isinstance(ast_node.children[-1], DP.TestlistContext):
        right_instr = build_test_list(block, ast_node.children[-1])
    else:
        right_instr = build_yield_expr(block, ast_node.children[-1])

    # get the operator without the "=" at the end
    op_text = ast_node_text(aug_node)[:-1]
    op_cls = math_operator_classes[op_text]
    op_instr = op_cls(block=block, ast_node=aug_node, left_instr=left_instr, right_instr=right_instr)
    block.add_instr(op_instr)

    assign = Assign(block=block, ast_node=aug_node, left_instr=left_instr, right_instr=op_instr)
    block.add_instr(assign)

    return assign


def build_assign_stmt(block, ast_node):
    left = build_test_star_stmt(block, ast_node.children[0])
    right = build_test_star_stmt(block, ast_node.children[2])
    assign = Assign(block, ast_node.children[1], left_instr=left, right_instr=right)
    block.add_instr(assign)
    return assign


def build_test_star_stmt(block, ast_node):
    # testlist_star_expr: (test | star_expr)(','(test | star_expr)) * (',')?;
    child_instrs = []
    for child in ast_node.children:
        if isinstance(child, antlr4.TerminalNode):
            continue  # skip commas in list
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
    star = CollapseStarExpr(block, ast_node, expr)
    block.add_instr(star)
    return star


def build_test_list(block, ast_node):
    # testlist: test (',' test)* (',')?;
    tests = []
    for i in range(0, len(ast_node.children), 2):
        test = build_test_stmt(block, ast_node.children[i])
        tests.append(test)
    return tests


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


def build_expression_list(block, ast_node):
    instr_list = []

    # exprlist: (expr | star_expr) (','(expr | star_expr))* (',')?;
    childs = ast_node.children
    while childs:
        node, *childs = childs
        if isinstance(node, DP.ExprContext):
            instr = build_expression(block, node)
        else:
            instr = build_star_expr(block, node)

        instr_list.append(instr)

        if childs:  # eat comma
            comma, *childs = childs

    if len(instr_list) == 1:
        return instr_list[0]

    return InstrList(block, ast_node, instr_list)


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

    childs = ast_node.children[1:]
    while len(childs) > 0:
        op_node, right_node, *childs = childs
        right_expr = build_term_expr(block, right_node)
        op_text = ast_node_text(op_node)
        instr_class = arith_operator_classes[op_text]
        instr = instr_class(block=block, ast_node=op_node, left_instr=left_expr, right_instr=right_expr)
        block.add_instr(instr)
        left_expr = instr

    return left_expr


def build_term_expr(block, ast_node):
    # term: factor(('*' | '@' | '/' | '%' | '//') factor) *;
    left_expr = build_factor_expr(block, ast_node.children[0])
    if len(ast_node.children) == 1:
        return left_expr

    childs = ast_node.children[1:]
    while len(childs) > 0:
        op_node, right_node, *childs = childs
        right_expr = build_factor_expr(block, right_node)
        op_text = ast_node_text(op_node)
        instr_class = term_operator_classes[op_text]
        instr = instr_class(block=block, ast_node=op_node, left_instr=left_expr, right_instr=right_expr)
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
    atom_instr = build_atom(block, atom_node)

    for trailer in trailers:
        atom_instr = build_atom_trailer(block, atom_instr, trailer)

    return atom_instr


def build_atom_trailer(block, atom, ast_node):
    # trailer: '('(arglist)? ')' | '[' subscriptlist ']' | '.' NAME;
    # Array / Dict subscript notation
    first_char = ast_node_text(ast_node.children[0])
    if first_char == '[':
        return build_subscript_list(block, atom, ast_node.children[1])
    elif first_char == '.':
        bare_name = BareName(block=block, ast_node=ast_node.children[1], text=ast_node_text(ast_node.children[1]))
        dot_op = DotOperator(block=block, ast_node=ast_node, left_instr=atom, right_instr=bare_name)
        block.add_instr(dot_op)
        return dot_op
    elif first_char == '(':  # function call
        args = []
        if len(ast_node.children) == 3:
            args = build_func_arg_list(block, ast_node.children[1])
        return FuncCall(block=block, ast_node=ast_node.children[0],
                        func_ptr_instr=atom, args=args)


def build_func_arg_list(block, ast_node):
    # arglist: argument(',' argument)*(',')?;
    args = []
    childs = ast_node.children
    while len(childs) > 0:
        arg_node, *childs = childs
        args.append(build_func_arg(block, arg_node))

        if len(childs) > 0:
            comma, *childs = childs

    return args


def build_func_arg(block, ast_node):
    # argument: (test (comp_for)? | test '=' test | '**' test | '*' test);
    childs = ast_node.children
    if len(childs) == 3:  # test = test
        left = build_test_stmt(childs[0])
        right = build_test_stmt(childs[2])
        return KeyWordArg(block, childs[0], left_instr=left, right_instr=right)

    if isinstance(childs[0], DP.TestContext):
        test_node, *childs = childs
        test_instr = build_test_stmt(block, test_node)
        if len(childs) == 0:
            return test_instr

        assert len(childs) == 1 and isinstance(childs[0], DP.Comp_forContext)
        generator_node = childs[0]
        return build_generator_expr(block, test_instr, generator_node)

    else:  # either *args or **kwargs style var
        text = ast_node_text(childs[0])
        child_instr = build_test_stmt(block, childs[1])
        if text == "**":
            return KeyWordArgVar(block=block, ast_node=childs[1], child_instr=child_instr)
        else:
            return ArgListVar(block=block, ast_node=childs[1], child_instr=child_instr)


def build_subscript_list(block, left_instr, ast_node):
    """
    subscriptlist: subscript (',' subscript)* (',')?;
    subscript: test | slice_expr;
    slice_expr: (test)? ':' (test)? (':' (test)?)?;
    """
    childs = ast_node.children
    subscripts = []

    while len(childs) > 0:
        subscr_node, *childs = childs
        instr = build_subscript_instr(block, subscr_node)
        subscripts.append(instr)

        if len(childs) > 0:
            comma, *childs = childs

    right_instr = SubscriptList(block=block, ast_node=ast_node, instrs=subscripts)
    block.add_instr(right_instr)

    instr = GetItem(block=block, ast_node=ast_node, left_instr=left_instr, right_instr=right_instr)
    block.add_instr(instr)
    return instr


def build_subscript_instr(block, ast_node):
    """
    subscript: test | slice_expr;
    slice_expr: (test)? ':'(test)? (':'(test)?)?;
    """
    top_node = ast_node.children[0]
    if isinstance(top_node, DP.TestContext):
        return build_test_stmt(block, top_node)

    # Otherwise, top node is a slice expr
    childs = top_node.children

    instrs = [None, None, None]
    instr_idx = 0
    while len(childs) > 0:
        if isinstance(childs[0], DP.TestContext):
            instr_node, *childs = childs
            instrs[instr_idx] = build_test_stmt(block, instr_node)

        if len(childs) > 0:  # move past colon
            colon, *childs = childs

        instr_idx += 1

    slice_instr = SliceOp(block, ast_node, start=instrs[0], stop=instrs[1], stride=instrs[2])
    block.add_instr(slice_instr)
    return slice_instr


def build_atom(block, ast_node):
    child = ast_node.children[0]
    if isinstance(child, DP.LiteralContext):
        return build_literal(block, child)
    elif isinstance(child, DP.Bare_nameContext):
        return BareName(block, child, ast_node_text(child))
    elif isinstance(child, DP.Atom_list_exprContext):
        return build_atom_list_expr(block, child)
    elif isinstance(child, DP.Atom_dict_exprContext):
        return build_atom_dict_expr(block, child)
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
        value, dtype = float(text), 'float'
    elif isinstance(child, DP.Bool_literalContext):
        value, dtype = (text == "true"), 'bool'
    elif isinstance(child, DP.None_literalContext):
        value, dtype = None, 'none'
    else:
        raise_unknown_ast_node(block, ast_node)

    literal = Literal(block=block, ast_node=child.children[0], dtype=dtype, value=value)
    block.add_instr(literal)
    return literal


def build_atom_list_expr(block, ast_node):
    # atom_list_expr: '[' (testlist_comp)? ']';
    args = None
    if len(ast_node.children) == 3:
        args = build_test_list_comp(block, ast_node.children[1])

    list_name = BareName(block=block, ast_node=ast_node.children[0], text="list")
    instr = FuncCall(block, ast_node, func_ptr_instr=list_name, args=args)
    block.add_instr(instr)
    return instr


def build_test_list_comp(block, ast_node):
    # testlist_comp: list_maker_items | list_maker_comp
    child = ast_node.children[0]
    if isinstance(child, DP.List_maker_compContext):
        return build_list_maker_comp(block, child)
    else:
        return build_list_maker_items(block, child)


def build_list_maker_items(block, ast_node):
    # list_maker_items: (test | star_expr)(','(test | star_expr)) * (',')?;
    child_instrs = []
    childs = ast_node.children
    while childs:
        first, *childs = childs
        if isinstance(first, DP.TestContext):
            instr = build_test_stmt(block, first)
        else:
            instr = build_star_expr(block, first)

        child_instrs.append(instr)

        if childs:  # eat comma
            comma, *childs = childs

    instr_list = InstrList(block, ast_node, child_instrs)
    block.add_instr(instr_list)
    return instr_list


def build_list_maker_comp(block, ast_node):
    # list_maker_comp: (test | star_expr) comp_for ;
    child = ast_node.children[0]

    comprehension = ListComprehension(block, ast_node)
    for_loop = build_comprehension_for_loop(block, ast_node.children[1])
    comprehension.for_loop = for_loop

    if isinstance(child, DP.TestContext):
        instr = build_test_stmt(for_loop, child)
    else:
        instr = build_star_expr(for_loop, child)

    comprehension.item_instr = instr

    block.add_instr(comprehension)
    return comprehension


def build_atom_gen_expr(block, ast_node):
    # atom_gen_expr: '('(yield_expr | testlist_comp)? ')';
    pass


def build_atom_dict_expr(block, ast_node):
    # atom_dict_expr: '{'(dictorsetmaker)? '}';
    is_dict = True
    args = None

    # If we have a middle child between braces, constructor args
    if len(ast_node.children) > 2:
        args_node = ast_node.children[1]
        is_dict = isinstance(args_node, DP.Dict_makerContext)
        if is_dict:
            args = build_dict_maker(block, args_node)
        else:
            args = build_set_maker(block, args_node)

    ctor_name = "dict" if is_dict else "set"
    dict_name = BareName(block=block, ast_node=ast_node.children[0], text=ctor_name)
    instr = FuncCall(block, ast_node, func_ptr_instr=dict_name, args=args)
    block.add_instr(instr)
    return instr


def build_dict_maker(block, ast_node):
    """
    dict_maker: dict_maker_key_vals | dict_maker_comp ;
    """
    node = ast_node.children[0]
    if isinstance(node, DP.Dict_maker_key_valsContext):
        return build_dict_maker_key_vals(block, node)
    else:
        return build_dict_maker_comprehension(block, node)


def build_dict_maker_key_vals(block, ast_node):
    """
    dict_maker_key_vals: (test ':' test | '**' expr) (',' (test ':' test | '**' expr))* (',')?;
    """
    childs = ast_node.children
    child_instrs = []
    while childs:
        node, *childs = childs
        # first check `test : test` idiom
        if isinstance(node, DP.TestContext):
            key_instr = build_test_stmt(block, node)
            colon, value_node, *childs = childs
            value_instr = build_test_stmt(block, value_node)
            instr = KeyValuePair(block, node, left_instr=key_instr, right_instr=value_instr)

        else:   # must be **kwargs idiom
            expr_node, *childs = childs
            expr_instr = build_expr_stmt(block, expr_node)
            instr = KeyValueExpand(block, ast_node=node, child_instr=expr_instr)

        block.add_instr(instr)
        child_instrs.append(instr)

        if childs:  # move past separator comma
            comma, *childs = childs

    instr = KeyValueList(block, ast_node, child_instrs)
    block.add_instr(instr)
    return instr


def build_dict_maker_comprehension(block, ast_node):
    """
    dict_maker_comp: (test ':' test | '**' expr) comp_for;
    """

    childs = ast_node.children

    dict_comp = DictComprehension(block, ast_node)
    block.add_instr(dict_comp)

    for_loop = build_comprehension_for_loop(block, childs[-1])
    dict_comp.for_loop = for_loop

    # Check for `test : test` idiom
    if isinstance(childs[0], DP.TestContext):
        key_node, colon, value_node, *_ = childs
        key_instr = build_test_stmt(for_loop, key_node)
        value_instr = build_test_stmt(for_loop, value_node)
        dict_comp.kvp_instr = KeyValuePair(for_loop, key_node, key_instr, value_instr)

    else:  # must start with **kwarg notation
        star_node, expr_node, *_ = childs
        expr_instr = build_expression(for_loop, expr_node)
        dict_comp.kvp_instr = KeyValueExpand(for_loop, star_node, expr_instr)

    return dict_comp


def build_comprehension_for_loop(block, ast_node):
    # comp_for: (ASYNC)? 'for' exprlist 'in' or_test (comp_iter)?;
    childs = ast_node.children

    if ast_text_is(childs[0], "async"):
        await_node, *childs = childs

    for_loop_block = ForLoop()
    block.add_instr(for_loop_block)

    for_, expr_list, in_, or_test, *comp_iter = childs

    for_loop_block.iter_vars = build_expression_list(for_loop_block, expr_list)
    iter_instr = build_logical_or_test(for_loop_block, or_test)
    for_loop_block.iter_src = iter_instr

    if comp_iter:
        build_comprehension_iter(for_loop_block, comp_iter[0])

    return for_loop_block


def build_comprehension_iter(block, ast_node):
    # comp_iter: comp_for | comp_if;
    child = ast_node.children[0]
    if isinstance(child, DP.Comp_forContext):
        return build_comprehension_for_loop(block, child)
    else:
        return build_comprehension_if_stmt(block, child)


def build_test_nocond(block, ast_node):
    # test_nocond: or_test | lambdef_nocond;
    child = ast_node.children[0]
    if isinstance(child, DP.Or_testContext):
        return build_logical_or_test(block, child)
    else:
        raise_unknown_ast_node(block, child)


def build_comprehension_if_stmt(block, ast_node):
    # comp_if: 'if' test_nocond (comp_iter)?;
    if_, test_node, *comp_iter = ast_node.children

    block.filter_cond = build_test_nocond(block, test_node)

    if comp_iter:
        build_comprehension_iter(block, comp_iter[0])


def build_set_maker(block, ast_node):
    # set_maker: set_maker_values | set_maker_comp;
    child = ast_node.children[0]
    if isinstance(child, DP.Set_maker_valuesContext):
        return build_set_maker_values(block, child)
    else:
        return build_set_maker_comprehension(block, child)


def build_set_maker_values(block, ast_node):
    # set_maker_values: (test | star_expr) (',' (test | star_expr))* (',')?;
    childs = ast_node.children
    child_instrs = []
    while childs:
        node, *childs = childs

        if isinstance(node, DP.TestContext):
            instr = build_test_stmt(block, node)
        else:
            instr = build_star_expr(block, node)

        block.add_instr(instr)
        child_instrs.append(instr)

        if childs:   # eat comma
            comma, *childs = childs

    return child_instrs


def build_set_maker_comprehension(block, ast_node):
    # set_maker_comp: (test | star_expr) comp_for;
    child = ast_node.children[0]

    comprehension = SetComprehension(block, ast_node)
    for_loop = build_comprehension_for_loop(block, ast_node.children[1])
    comprehension.for_loop = for_loop

    if isinstance(child, DP.TestContext):
        instr = build_test_stmt(for_loop, child)
    else:
        instr = build_star_expr(for_loop, child)

    comprehension.item_instr = instr

    block.add_instr(comprehension)
    return comprehension


def build_compound_stmt(block, ast_stmt):
    # compound_stmt: if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt;
    for child in ast_stmt.children:
        if isinstance(child, DP.If_stmtContext):
            build_if_statement(block, child)
        elif isinstance(child, DP.While_stmtContext):
            build_while_loop_statement(block, child)
        elif isinstance(child, DP.Do_while_stmtContext):
            build_do_while_loop_statement(block, child)
        elif isinstance(child, DP.For_stmtContext):
            build_forloop_statement(block, child)
        elif isinstance(child, DP.Try_stmtContext):
            build_try_catch_statement(block, child)
        elif isinstance(child, DP.With_stmtContext):
            build_with_statement(block, child)
        elif isinstance(child, DP.FuncdefContext):
            build_func_def(block, child)
        elif isinstance(child, DP.ClassdefContext):
            build_classdef(block, child)
        elif isinstance(child, DP.DecoratedContext):
            build_decorated_stmt(block, child)
        elif isinstance(child, DP.Async_stmtContext):
            build_async_stmt(block, child)
        else:
            raise_unknown_ast_node(block, child)


def build_while_loop_statement(block, ast_node):
    # while_stmt: 'while' test ':' suite;
    cond = build_test_stmt(block, ast_node.children[1])
    while_block = WhileLoop(parent=block, ast_node=ast_node, cond=cond)
    build_suite(while_block, ast_node.children[3])
    block.add_instr(while_block)
    return while_block


def build_do_while_loop_statement(block, ast_node):
    # do_while_stmt: 'do' ':' suite 'while' test ;
    cond = build_test_stmt(block, ast_node.children[-1])
    while_block = DoWhileLoop(parent=block, ast_node=ast_node, cond=cond)
    build_suite(while_block, ast_node.children[2])
    block.add_instr(while_block)
    return while_block


def build_forloop_statement(block, ast_node):
    # for_stmt: 'for' exprlist 'in' testlist ':' suite ;
    iter_vars = build_expression_list(block, ast_node.children[1])
    iter_src = build_test_list(block, ast_node.children[3])
    for_block = ForLoop(ast_node=ast_node, parent=block, iter_vars=iter_vars, iter_src=iter_src)
    build_suite(for_block, ast_node.children[-1])
    block.add_instr(for_block)
    return for_block


def build_try_catch_statement(block, ast_node):
    pass


def build_if_statement(block, ast_node):
    #  if_stmt: 'if' test ':' suite ('elif' test ':' suite)* ('else' ':' suite)?;
    childs = ast_node.children
    cond = build_test_stmt(block, childs[1])
    if_block = IfCondition(cond=cond, parent=block, ast_node=ast_node)
    build_suite(if_block, childs[3])

    childs = childs[4:]
    while childs:
        if ast_node_text(childs[0]) == 'else':
            else_block = ElseBlock(parent=block, ast_node=childs[0])
            if_block.else_block = else_block
            build_suite(else_block, childs[2])
            break
        else:
            cond = build_test_stmt(block, childs[1])
            elif_block = ElifCondition(parent=block, ast_node=childs[0], cond=cond)
            build_suite(elif_block, childs[3])
            childs = childs[4:]
            if_block.add_elif(elif_block)

    block.add_instr(if_block)
    return if_block

def build_classdef(block, ast_node):
    # 'class' NAME ('(' (arglist)? ')')? ':' suite;
    class_name = ast_node_text(ast_node.children[1])

    supers = []
    for child in ast_node.children:
        if isinstance(child, DP.ArglistContext):
            supers = build_func_arg_list(block, child)
            break

    class_instr = ClassDef(parent=block, ast_node=ast_node, class_name=class_name, supers=supers)
    class_instr.body = build_suite(class_instr, ast_node.children[-1])
    block.add_instr(class_instr)


def build_func_def(block, ast_node):
    # funcdef: 'def' NAME parameters ('->' test)? ':' suite;

    def_, func_name, params, *childs = ast_node.children
    *childs, colon_, suite = childs

    returns = None
    if childs:  # have unparsed tokens, is "-> <return>"
        arrow_, ret_type = childs
        returns = build_test_stmt(block, ret_type)

    name_instr = ast_node_text(func_name)
    params_instr = build_parameters(block, params)
    func = FuncDef(ast_node=ast_node, parent=block, name=name_instr, params=params_instr, returns=returns)
    func.body = build_suite(func, ast_node.children[-1])
    block.add_instr(func)
    return func


def build_parameters(block, ast_node):
    # parameters: '(' (typedargslist)? ')';

    # if only two children, just parens, no params
    if len(ast_node.children) < 3:
        return []

    return build_typedargs_list(block, ast_node.children[1])


def build_typedargs_list(block, ast_node):
    """
    typedargslist: typedarg_item (',' typedarg_item)* (',')?;
    """
    args = []
    childs = ast_node.children
    while childs:
        typedarg_node, *childs = childs
        instr = build_typedarg_item(block, typedarg_node)
        args.append(instr)
        if childs:
            comma_, *childs = childs

    return args


def build_typedarg_item(block, ast_node):
    # typedarg_item: namedarg | star_args | named_kw_args
    child = ast_node.children[0]
    if isinstance(child, DP.NamedargContext):
        return build_named_arg(block, child)
    elif isinstance(child, DP.Star_argsContext):
        return build_star_args(block, child)
    elif isinstance(child, DP.Named_kw_argsContext):
        return build_kw_args(block, child)
    else:
        raise_unknown_ast_node(block, child)


def build_named_arg(block, ast_node):
    # namedarg: type_qual? NAME ('=' test) ? ;
    childs = ast_node.children

    type_qual, default_value = None, None

    if isinstance(childs[0], DP.Type_qualContext):
        type_qual, *childs = childs
        type_qual = build_type_qual(block, type_qual)

    name, childs = ast_node_text(childs[0]), childs[1:]

    if childs:  # has a test statement
        default_value = build_test_stmt(block, childs[1])

    return NamedFuncArg(block=block, ast_node=ast_node,
                        name=name, type_qual=type_qual, default_value=default_value)


def build_type_qual(block, ast_node):
    # type_qual: NAME (template_def)? ;
    type_name = ast_node_text(ast_node.children[0])
    template_def = None
    if len(ast_node.children) > 1:
        template_def = build_template_def(block, ast_node.children[1])

    return TypeQualifier(block, ast_node, type_name, template_def)


def build_template_def(block, ast_node):
    # template_def: '<' (template_args)? '>' ;
    # template_args: NAME (',' NAME)* ','?;
    if len(ast_node.children) == 2:
        return TemplateDef(block, ast_node, [])

    args = ast_node.children[1].children
    arg_names = []
    while args:
        first_arg, *args = args
        arg_names.append(ast_node_text(first_arg))
        if args:
            comma_, *args = args

    return TemplateDef(block, ast_node, arg_names)


def build_star_args(block, ast_node):
    # star_args: type_qual? '*' NAME ;
    type_qual = None
    if len(ast_node.children) > 2:
        type_qual = build_type_qual(block, ast_node.children[0])

    name = ast_node_text(ast_node.children[-1])
    return StarFuncArg(block, ast_node, name, type_qual)


def build_kw_args(block, ast_node):
    # named_kw_args: type_qual? '**' NAME ;
    type_qual = None
    if len(ast_node.children) > 2:
        type_qual = build_type_qual(block, ast_node.children[0])

    name = ast_node_text(ast_node.children[-1])
    return StarKwFuncArg(block, ast_node, name, type_qual)


def build_suite(block, ast_node):
    #  suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT;
    if len(ast_node.children) == 1:
        return [ build_simple_stmt(block, ast_node.children[1]) ]

    stmts = []
    stmt_nodes = ast_node.children[2:-1]
    for stmt_node in stmt_nodes:
        stmt_instr = build_statement(block, stmt_node)
        stmts.append(stmt_instr)

    return stmts


def term_text_equals(term_node, text):
    return isinstance(term_node, antlr4.TerminalNode) and term_node.symbol.text == text
