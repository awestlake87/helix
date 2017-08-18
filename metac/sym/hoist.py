from ..ast import *

from .scope import Scope
from .fun_symbol import *
from .struct_symbol import *
from .var_symbol import *

from ..err import Todo

def hoist_block(unit, block):
    assert block.scope is None

    block.scope = Scope(unit.scope)

    with unit.use_scope(block.scope):
        for statement in block.statements:
            statement_type = type(statement)

            if issubclass(statement_type, ExprNode):
                hoist_expr(unit, statement)

            elif statement_type is IfStatementNode:
                hoist_if_statement(unit, statement)

            elif statement_type is LoopStatementNode:
                hoist_loop_statement(unit, statement)

            elif statement_type is SwitchStatementNode:
                hoist_switch_statement(unit, statement)

            elif statement_type is ReturnNode:
                hoist_return_statement(unit, statement)

            elif statement_type is BreakNode or statement_type is ContinueNode:
                pass
                
            else:
                raise Todo()

def hoist_expr(unit, expr):
    expr_type = type(expr)

    if expr_type is StructNode:
        hoist_struct(unit, expr)

    elif expr_type is FunNode:
        hoist_fun(unit, expr)

    elif expr_type is CallExprNode:
        hoist_call(unit, expr)

    elif expr_type is InitExprNode:
        hoist_init(unit, expr)

    elif expr_type is DotExprNode:
        pass

    elif expr_type is TernaryConditionalNode:
        hoist_ternary_conditional(unit, expr)

    elif issubclass(expr_type, UnaryExprNode):
        hoist_unary_expr(unit, expr)

    elif issubclass(expr_type, BinaryExprNode):
        hoist_binary_expr(unit, expr)

    elif expr_type is FunTypeNode:
        hoist_fun_type(unit, expr)

    elif expr_type is SymbolNode:
        # outside of the proper context, these are just refs
        pass

    elif expr_type is IntTypeNode:
        # just stock integer types
        pass

    elif issubclass(expr_type, LiteralNode):
        # meta literals don't need hoisting
        pass

    else:
        raise Todo(repr(expr))

def hoist_unary_expr(unit, expr):
    hoist_expr(unit, expr.operand)

def hoist_binary_expr(unit, expr):
    hoist_expr(unit, expr.lhs)
    hoist_expr(unit, expr.rhs)

def hoist_call(unit, expr):
    hoist_expr(unit, expr.lhs)

    for arg in expr.args:
        hoist_expr(unit, arg)

def hoist_init(unit, expr):
    if type(expr.lhs) is SymbolNode:
        hoist_expr(unit, expr.rhs)
        unit.scope.insert(expr.lhs.id, VarSymbol())

    else:
        raise Todo()

def hoist_ternary_conditional(unit, expr):
    hoist_expr(unit, expr.lhs)
    hoist_expr(unit, expr.condition)
    hoist_expr(unit, expr.rhs)

def hoist_struct(unit, s):
    unit.scope.insert(s.id, StructSymbol(unit, unit.scope, s))

def hoist_fun(unit, f):
    symbol = FunSymbol(unit, f, unit.scope)
    unit.scope.insert(f.id, symbol)

    hoist_expr(unit, f.type)

    for param in symbol.ast.param_ids:
        symbol.scope.insert(param, VarSymbol())

    with unit.use_scope(symbol.scope):
        hoist_block(unit, symbol.ast.body)

def hoist_fun_type(unit, fun_type):
    hoist_expr(unit, fun_type.ret_type)

    for param in fun_type.param_types:
        hoist_expr(unit, param)

def hoist_if_statement(unit, statement):
    assert statement.scope is None

    statement.scope = Scope(unit.scope)

    with unit.use_scope(statement.scope):
        for condition, block in statement.if_branches:
            hoist_expr(unit, condition)
            hoist_block(unit, block)

        if statement.else_block is not None:
            hoist_block(unit, statement.else_block)

def hoist_loop_statement(unit, statement):
    assert statement.scope is None

    statement.scope = Scope(unit.scope)

    with unit.use_scope(statement.scope):
        if statement.for_clause is not None:
            hoist_expr(unit, statement.for_clause)

        if statement.each_clause is not None:
            hoist_expr(unit, statement.each_clause)

        if statement.while_clause is not None:
            hoist_expr(unit, statement.while_clause)

        if statement.loop_body is not None:
            hoist_block(unit, statement.loop_body)

        if statement.then_clause is not None:
            hoist_expr(unit, statement.then_clause)

        if statement.until_clause is not None:
            hoist_expr(unit, statement.until_clause)

def hoist_switch_statement(unit, statement):
    assert statement.scope is None

    statement.scope = Scope(unit.scope)

    with unit.use_scope(statement.scope):
        for case_value, case_block in statement.case_branches:
            hoist_expr(unit, case_value)
            hoist_block(unit, case_block)

        if statement.default_block is not None:
            hoist_block(unit, statement.default_block)


def hoist_return_statement(unit, statement):
    hoist_expr(unit, statement.expr)
