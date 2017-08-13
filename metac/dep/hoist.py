from ..ast import *

from .symbols import *

from ..err import Todo

def hoist(scope, ast):
    hoist_block(scope, ast)

def hoist_block(scope, block):
    for statement in block.statements:
        statement_type = type(statement)
        if issubclass(statement_type, ExprNode):
            hoist_expr(scope, statement)

        elif statement_type is IfStatementNode:
            hoist_if_statement(scope, statement)

        elif statement_type is ReturnNode:
            hoist_return(scope, statement)

        else:
            raise Todo()


def hoist_expr(scope, expr):
    expr_type = type(expr)

    if expr_type is StructNode:
        hoist_struct(scope, expr)

    elif expr_type is FunNode:
        hoist_fun(scope, expr)

    elif expr_type is CallExprNode:
        hoist_call_expr(scope, expr)

    elif expr_type is InitExprNode:
        hoist_init_expr(scope, expr)

    elif expr_type is DotExprNode:
        pass

    elif issubclass(expr_type, UnaryExprNode):
        hoist_unary(scope, expr)

    elif issubclass(expr_type, BinaryExprNode):
        hoist_binary(scope, expr)

    elif expr_type is FunTypeNode:
        hoist_fun_type(scope, expr)

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

def hoist_unary(scope, expr):
    hoist_expr(scope, expr.operand)

def hoist_binary(scope, expr):
    hoist_expr(scope, expr.lhs)
    hoist_expr(scope, expr.rhs)

def hoist_call_expr(scope, expr):
    hoist_expr(scope, expr.lhs)

    for arg in expr.args:
        hoist_expr(scope, expr.args)

def hoist_init_expr(scope, expr):
    if type(expr.lhs) is SymbolNode:
        hoist_expr(scope, expr.rhs)
        scope.insert(expr.lhs.id, VarSymbol())

    else:
        raise Todo()

def hoist_struct(scope, s):
    scope.insert(s.id, StructSymbol(scope, s))

def hoist_fun(scope, f):
    symbol = FunSymbol(f, scope)
    scope.insert(f.id, symbol)

    hoist_expr(scope, f.type)

    for param in symbol.ast.param_ids:
        symbol.scope.insert(param, VarSymbol())

    hoist_block(symbol.scope, symbol.ast.body)

def hoist_fun_type(scope, fun_type):
    hoist_expr(scope, fun_type.ret_type)

    for param in fun_type.param_types:
        hoist_expr(scope, fun_type.param_types)

def hoist_if_statement(scope, statement):
    raise Todo()

def hoist_return(scope, statement):
    hoist_expr(scope, statement.expr)
