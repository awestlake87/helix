from ..ast import *
from ..err import Todo

from .scope import Scope
from .values import *

def hoist_block(unit, block):
    assert block.scope is None

    block.scope = Scope(unit.scope)

    with unit.use_scope(block.scope):
        for statement in block.statements:
            statement_type = type(statement)

            if issubclass(statement_type, ExprNode):
                hoist_expr(unit, statement)

            elif statement_type is IfNode:
                hoist_if_statement(unit, statement)

            elif statement_type is LoopNode:
                hoist_loop_statement(unit, statement)

            elif statement_type is SwitchNode:
                hoist_switch_statement(unit, statement)

            elif statement_type is ReturnNode:
                hoist_return_statement(unit, statement)

            elif statement_type is TryNode:
                hoist_try_statement(unit, statement)

            elif statement_type is ThrowStatementNode:
                hoist_expr(unit, statement.expr)

            elif statement_type is BreakNode or statement_type is ContinueNode:
                pass

            elif statement_type is BlockNode:
                hoist_block(unit, statement)

            else:
                raise Todo(statement_type)

def hoist_expr(unit, expr):
    expr_type = type(expr)

    if expr_type is StructNode:
        hoist_struct(unit, expr)

    elif expr_type is FunNode:
        hoist_fun(unit, expr)

    elif expr_type is CallNode:
        hoist_call(unit, expr)

    elif expr_type is EmbedCallNode:
        hoist_call(unit, expr)

    elif expr_type is InitNode:
        hoist_init(unit, expr)

    elif expr_type is DotNode:
        pass

    elif expr_type is OffsetofNode:
        hoist_expr(unit, expr.lhs)

    elif expr_type is ArrayTypeNode:
        hoist_expr(unit, expr.length)
        hoist_expr(unit, expr.type)

    elif expr_type is TernaryConditionalNode:
        hoist_ternary_conditional(unit, expr)

    elif expr_type is GlobalNode:
        hoist_global_expr(unit, expr)

    elif issubclass(expr_type, UnaryExprNode):
        hoist_unary_expr(unit, expr)

    elif issubclass(expr_type, BinaryExprNode):
        hoist_binary_expr(unit, expr)

    elif expr_type is FunTypeNode:
        hoist_fun_type(unit, expr)

    elif expr_type is SymbolNode or expr_type is AttrNode:
        # outside of the proper context, these are just refs
        pass

    elif expr_type is IntTypeNode:
        # just stock integer types
        pass

    elif expr_type is VoidTypeNode:
        pass

    elif expr_type is AutoTypeNode:
        pass

    elif issubclass(expr_type, LiteralNode):
        # literals don't need hoisting
        pass

    else:
        raise Todo(repr(expr))

def hoist_global_expr(unit, expr):
    hoist_expr(unit, expr.type)
    unit.scope.insert(expr.id, GlobalSym(unit, expr, unit.scope))

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
        unit.scope.insert(expr.lhs.id, VarSym())

    elif type(expr.lhs) is GlobalNode:
        hoist_expr(unit, expr.lhs)
        hoist_expr(unit, expr.rhs)
        unit.scope.resolve(expr.lhs.id).init_expr = expr.rhs

    else:
        raise Todo()

def hoist_ternary_conditional(unit, expr):
    hoist_expr(unit, expr.lhs)
    hoist_expr(unit, expr.condition)
    hoist_expr(unit, expr.rhs)

def hoist_struct(unit, s):
    symbol = StructSym(unit, unit.scope, s)
    unit.scope.insert(s.id, symbol)

    with unit.use_scope(symbol.scope):
        for attr_id, attr_symbol in symbol.attrs:
            if issubclass(type(attr_symbol), AttrFunSym):
                hoist_expr(unit, attr_symbol.ast.type)

                for param in attr_symbol.ast.param_ids:
                    attr_symbol.scope.insert(param, VarSym())

                if attr_symbol.ast.body is not None:
                    with unit.use_scope(attr_symbol.scope):
                        hoist_block(unit, attr_symbol.ast.body)

            elif type(attr_symbol) is FunSym:
                hoist_fun(unit, attr_symbol.ast)

            elif type(attr_symbol) is DataAttrSym:
                pass

            else:
                raise Todo(attr_symbol)


def hoist_fun(unit, f):
    symbol = FunSym(unit, f, unit.scope)
    unit.scope.insert(f.id, symbol)

    hoist_expr(unit, f.type)

    for param in symbol.ast.param_ids:
        symbol.scope.insert(param, VarSym())

    if symbol.ast.body is not None:
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
        for case_values, case_block in statement.case_branches:
            for value in case_values:
                hoist_expr(unit, value)

            hoist_block(unit, case_block)

        if statement.default_block is not None:
            hoist_block(unit, statement.default_block)


def hoist_return_statement(unit, statement):
    if statement.expr is not None:
        hoist_expr(unit, statement.expr)

def hoist_try_statement(unit, statement):
    hoist_block(unit, statement.try_block)

    for clause in statement.catch_clauses:
        assert clause.scope is None

        clause.scope = Scope(unit.scope)

        with unit.use_scope(clause.scope):
            hoist_expr(unit, clause.type)

            unit.scope.insert(clause.id, VarSym())

            hoist_block(unit, clause.block)

    if statement.default_catch is not None:
        hoist_block(unit, statement.default_catch)
