
from ..ast import *
from ..err import *

def get_block_deps(scope, block):
    deps = [ ]
    for statement in block.statements:
        deps += get_statement_deps(scope, statement)

    return deps

def get_statement_deps(scope, statement):
    statement_type = type(statement)

    if statement_type is StructNode or statement_type is FunNode:
        # standalone structs or funs are not deps
        return [ ]

    elif issubclass(statement_type, ExprNode):
        return get_expr_deps(scope, statement)

    elif statement_type is ReturnNode:
        return get_return_deps(scope, statement)

    else:
        raise Todo(repr(statement))

def get_expr_deps(scope, expr):
    expr_type = type(expr)

    if expr_type is StructNode:
        raise Todo("struct node is used")

    if expr_type is FunNode:
        raise Todo("fun node is used")

    elif expr_type is CallExprNode:
        return get_call_deps(scope, expr)

    elif expr_type is DotExprNode:
        return [ ]

    elif issubclass(expr_type, UnaryExprNode):
        return get_unary_expr_deps(scope, expr)

    elif issubclass(expr_type, BinaryExprNode):
        return get_binary_expr_deps(scope, expr)

    elif expr_type is SymbolNode:
        return [ scope.resolve(expr.id).get_target() ]

    elif expr_type is FunTypeNode:
        return get_fun_type_deps(scope, expr)

    elif expr_type is IntTypeNode:
        return [ ]

    elif issubclass(expr_type, LiteralNode):
        return [ ]

    else:
        raise Todo(expr)

def get_unary_expr_deps(scope, expr):
    return get_expr_deps(expr.operand)

def get_binary_expr_deps(scope, expr):
    return get_expr_deps(scope, expr.lhs) + get_expr_deps(scope, expr.rhs)

def get_call_deps(scope, expr):
    deps = get_expr_deps(scope, expr.lhs)

    for arg in expr.args:
        deps += get_expr_deps(scope, arg)

    return deps

def get_fun_type_deps(scope, fun_type):
    deps = get_expr_deps(scope, fun_type.ret_type)

    for param in fun_type.param_types:
        deps += get_expr_deps(scope, param)

    return deps

def get_return_deps(scope, statement):
    return get_expr_deps(scope, statement.expr)
