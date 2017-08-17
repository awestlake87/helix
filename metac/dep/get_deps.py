
from ..ast import *
from ..err import *

def get_block_deps(unit, block):
    assert block.scope is not None

    with unit.use_scope(block.scope):
        deps = [ ]
        for statement in block.statements:
            deps += get_statement_deps(unit, statement)

        return deps

def get_statement_deps(unit, statement):
    statement_type = type(statement)

    if statement_type is ReturnNode:
        return get_return_deps(unit, statement)

    elif statement_type is IfStatementNode:
        return get_if_statement_deps(unit, statement)

    elif statement_type is LoopStatementNode:
        return get_loop_statement_deps(unit, statement)

    elif statement_type is SwitchStatementNode:
        return get_switch_statement_deps(unit, statement)

    elif statement_type is StructNode or statement_type is FunNode:
        # standalone structs or funs are not deps
        return [ ]

    elif issubclass(statement_type, ExprNode):
        return get_expr_deps(unit, statement)

    else:
        raise Todo(repr(statement))

def get_expr_deps(unit, expr):
    expr_type = type(expr)

    if expr_type is StructNode:
        raise Todo("struct node is used")

    if expr_type is FunNode:
        raise Todo("fun node is used")

    elif expr_type is CallExprNode:
        return get_call_deps(unit, expr)

    elif expr_type is DotExprNode:
        return [ ]

    elif issubclass(expr_type, UnaryExprNode):
        return get_unary_expr_deps(unit, expr)

    elif issubclass(expr_type, BinaryExprNode):
        return get_binary_expr_deps(unit, expr)

    elif expr_type is SymbolNode:
        return [ unit.scope.resolve(expr.id).get_target() ]

    elif expr_type is FunTypeNode:
        return get_fun_type_deps(unit, expr)

    elif expr_type is IntTypeNode:
        return [ ]

    elif issubclass(expr_type, LiteralNode):
        return [ ]

    else:
        raise Todo(expr)

def get_unary_expr_deps(unit, expr):
    return get_expr_deps(unit, expr.operand)

def get_binary_expr_deps(unit, expr):
    return get_expr_deps(unit, expr.lhs) + get_expr_deps(unit, expr.rhs)

def get_call_deps(unit, expr):
    deps = get_expr_deps(unit, expr.lhs)

    for arg in expr.args:
        deps += get_expr_deps(unit, arg)

    return deps

def get_fun_type_deps(unit, fun_type):
    deps = get_expr_deps(unit, fun_type.ret_type)

    for param in fun_type.param_types:
        deps += get_expr_deps(unit, param)

    return deps

def get_return_deps(unit, statement):
    return get_expr_deps(unit, statement.expr)

def get_if_statement_deps(unit, statement):
    assert statement.scope is not None

    deps = [ ]

    with unit.use_scope(statement.scope):
        for condition, block in statement.if_branches:
            deps += get_expr_deps(unit, condition)
            deps += get_block_deps(unit, block)

        if statement.else_block is not None:
            deps += get_block_deps(unit, statement.else_block)

    return deps

def get_loop_statement_deps(unit, statement):
    assert statement.scope is not None

    deps = [ ]

    with unit.use_scope(statement.scope):
        if statement.for_clause is not None:
            deps += get_expr_deps(unit, statement.for_clause)

        if statement.each_clause is not None:
            deps += get_expr_deps(unit, statement.each_clause)

        if statement.while_clause is not None:
            deps += get_expr_deps(unit, statement.while_clause)

        if statement.loop_body is not None:
            deps += get_block_deps(unit, statement.loop_body)

        if statement.then_clause is not None:
            deps += get_expr_deps(unit, statement.then_clause)

        if statement.until_clause is not None:
            deps += get_expr_deps(unit, statement.until_clause)

    return deps

def get_switch_statement_deps(unit, statement):
    assert statement.scope is not None

    deps = [ ]

    with unit.use_scope(statement.scope):
        for case_value, case_block in statement.case_branches:
            deps += get_expr_deps(unit, case_value)
            deps += get_block_deps(unit, case_block)

        if statement.default_block is not None:
            deps += get_block_deps(unit, statement.default_block)

    return deps
