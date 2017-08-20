
from ..ast import *
from ..err import *

def gen_block_deps(unit, block):
    assert block.scope is not None

    with unit.use_scope(block.scope):
        deps = [ ]
        for statement in block.statements:
            deps += gen_statement_deps(unit, statement)

        return deps

def gen_statement_deps(unit, statement):
    statement_type = type(statement)

    if statement_type is ReturnNode:
        return gen_return_deps(unit, statement)

    elif statement_type is IfStatementNode:
        return gen_if_statement_deps(unit, statement)

    elif statement_type is LoopStatementNode:
        return gen_loop_statement_deps(unit, statement)

    elif statement_type is SwitchStatementNode:
        return gen_switch_statement_deps(unit, statement)

    elif statement_type is BreakNode or statement_type is ContinueNode:
        return [ ]

    elif statement_type is StructNode or statement_type is FunNode:
        # standalone structs or funs are not deps
        return [ ]

    elif issubclass(statement_type, ExprNode):
        return gen_expr_deps(unit, statement)

    else:
        raise Todo(repr(statement))

def gen_expr_deps(unit, expr):
    expr_type = type(expr)

    if expr_type is StructNode:
        raise Todo("struct node is used")

    if expr_type is FunNode:
        raise Todo("fun node is used")

    elif expr_type is CallExprNode:
        return gen_call_deps(unit, expr)

    elif expr_type is DotExprNode:
        return [ ]

    elif expr_type is TernaryConditionalNode:
        return gen_ternary_conditional_deps(unit, expr)

    elif issubclass(expr_type, UnaryExprNode):
        return gen_unary_expr_deps(unit, expr)

    elif issubclass(expr_type, BinaryExprNode):
        return gen_binary_expr_deps(unit, expr)

    elif expr_type is SymbolNode:
        return [ unit.scope.resolve(expr.id).get_target() ]

    elif expr_type is FunTypeNode:
        return gen_fun_type_deps(unit, expr)

    elif expr_type is IntTypeNode:
        return [ ]

    elif issubclass(expr_type, LiteralNode):
        return [ ]

    else:
        raise Todo(expr)

def gen_unary_expr_deps(unit, expr):
    return gen_expr_deps(unit, expr.operand)

def gen_binary_expr_deps(unit, expr):
    return gen_expr_deps(unit, expr.lhs) + gen_expr_deps(unit, expr.rhs)

def gen_ternary_conditional_deps(unit, expr):
    return (
        gen_expr_deps(unit, expr.lhs) +
        gen_expr_deps(unit, expr.condition) +
        gen_expr_deps(unit, expr.rhs)
    )

def gen_call_deps(unit, expr):
    deps = gen_expr_deps(unit, expr.lhs)

    for arg in expr.args:
        deps += gen_expr_deps(unit, arg)

    return deps

def gen_fun_type_deps(unit, fun_type):
    deps = gen_expr_deps(unit, fun_type.ret_type)

    for param in fun_type.param_types:
        deps += gen_expr_deps(unit, param)

    return deps

def gen_return_deps(unit, statement):
    return gen_expr_deps(unit, statement.expr)

def gen_if_statement_deps(unit, statement):
    assert statement.scope is not None

    deps = [ ]

    with unit.use_scope(statement.scope):
        for condition, block in statement.if_branches:
            deps += gen_expr_deps(unit, condition)
            deps += gen_block_deps(unit, block)

        if statement.else_block is not None:
            deps += gen_block_deps(unit, statement.else_block)

    return deps

def gen_loop_statement_deps(unit, statement):
    assert statement.scope is not None

    deps = [ ]

    with unit.use_scope(statement.scope):
        if statement.for_clause is not None:
            deps += gen_expr_deps(unit, statement.for_clause)

        if statement.each_clause is not None:
            deps += gen_expr_deps(unit, statement.each_clause)

        if statement.while_clause is not None:
            deps += gen_expr_deps(unit, statement.while_clause)

        if statement.loop_body is not None:
            deps += gen_block_deps(unit, statement.loop_body)

        if statement.then_clause is not None:
            deps += gen_expr_deps(unit, statement.then_clause)

        if statement.until_clause is not None:
            deps += gen_expr_deps(unit, statement.until_clause)

    return deps

def gen_switch_statement_deps(unit, statement):
    assert statement.scope is not None

    deps = [ ]

    with unit.use_scope(statement.scope):
        for case_values, case_block in statement.case_branches:
            for value in case_values:
                deps += gen_expr_deps(unit, value)
            deps += gen_block_deps(unit, case_block)

        if statement.default_block is not None:
            deps += gen_block_deps(unit, statement.default_block)

    return deps
