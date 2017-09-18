from contextlib import contextmanager

from ..ast import *
from ..err import Todo

from .scope import Scope
from .values import *

def hoist(unit_node):
    class Context:
        def __init__(self, unit_sym):
            self.unit = unit_sym

            self.scope = None

        def set_scope(self, ast_node, scope):
            self.unit.set_scope(ast_node, scope)

        def get_scope(self, ast_node):
            return self.unit.get_scope(ast_node)

        @contextmanager
        def use_scope(self, scope):
            old_scope = self.scope
            self.scope = scope

            yield

            self.scope = old_scope

    unit_sym = UnitSym(unit_node.id, unit_node)
    ctx = Context(unit_sym)

    with ctx.use_scope(unit_sym.scope):
        hoist_block(ctx, unit_node.block)

    return unit_sym

def hoist_block(ctx, block):
    ctx.set_scope(block, Scope(ctx.scope))

    with ctx.use_scope(ctx.get_scope(block)):
        for statement in block.statements:
            statement_type = type(statement)

            if issubclass(statement_type, ExprNode):
                hoist_expr(ctx, statement)

            elif statement_type is IfNode:
                hoist_if_statement(ctx, statement)

            elif statement_type is LoopNode:
                hoist_loop_statement(ctx, statement)

            elif statement_type is SwitchNode:
                hoist_switch_statement(ctx, statement)

            elif statement_type is ReturnNode:
                hoist_return_statement(ctx, statement)

            elif statement_type is TryNode:
                hoist_try_statement(ctx, statement)

            elif statement_type is ThrowNode:
                hoist_expr(ctx, statement.expr)

            elif statement_type is BreakNode or statement_type is ContinueNode:
                pass

            elif statement_type is BlockNode:
                hoist_block(ctx, statement)

            else:
                raise Todo(statement_type)

def hoist_expr(ctx, expr):
    expr_type = type(expr)

    if expr_type is StructNode:
        hoist_struct(ctx, expr)

    elif expr_type is FunNode:
        hoist_fun(ctx, expr)

    elif expr_type is CallNode:
        hoist_call(ctx, expr)

    elif expr_type is EmbedCallNode:
        hoist_call(ctx, expr)

    elif expr_type is InitNode:
        hoist_init(ctx, expr)

    elif expr_type is DotNode:
        pass

    elif expr_type is OffsetofNode:
        hoist_expr(ctx, expr.lhs)

    elif expr_type is ArrayTypeNode:
        hoist_expr(ctx, expr.length)
        hoist_expr(ctx, expr.type)

    elif expr_type is TernaryConditionalNode:
        hoist_ternary_conditional(ctx, expr)

    elif expr_type is GlobalNode:
        hoist_global_expr(ctx, expr)

    elif issubclass(expr_type, UnaryExprNode):
        hoist_unary_expr(ctx, expr)

    elif issubclass(expr_type, BinaryExprNode):
        hoist_binary_expr(ctx, expr)

    elif expr_type is FunTypeNode:
        hoist_fun_type(ctx, expr)

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

def hoist_global_expr(ctx, expr):
    hoist_expr(ctx, expr.type)
    ctx.scope.insert(expr.id, GlobalSym(ctx.unit, expr, ctx.scope))

def hoist_unary_expr(ctx, expr):
    hoist_expr(ctx, expr.operand)

def hoist_binary_expr(ctx, expr):
    hoist_expr(ctx, expr.lhs)
    hoist_expr(ctx, expr.rhs)

def hoist_call(ctx, expr):
    hoist_expr(ctx, expr.lhs)

    for arg in expr.args:
        hoist_expr(ctx, arg)

def hoist_init(ctx, expr):
    lhs_type = type(expr.lhs)

    if lhs_type is SymbolNode:
        hoist_expr(ctx, expr.rhs)
        ctx.scope.insert(expr.lhs.id, VarSym())

    elif lhs_type is MutNode:
        if type(expr.lhs.operand) is SymbolNode:
            hoist_expr(ctx, expr.rhs)
            ctx.scope.insert(expr.lhs.operand.id, VarSym())

        else:
            raise Todo(type(expr.lhs.operand))


    elif lhs_type is GlobalNode:
        hoist_expr(ctx, expr.lhs)
        hoist_expr(ctx, expr.rhs)
        ctx.scope.resolve(expr.lhs.id).init_expr = expr.rhs

    else:
        raise Todo()

def hoist_ternary_conditional(ctx, expr):
    hoist_expr(ctx, expr.lhs)
    hoist_expr(ctx, expr.condition)
    hoist_expr(ctx, expr.rhs)

def hoist_struct(ctx, s):
    symbol = StructSym(ctx.unit, ctx.scope, s)
    ctx.scope.insert(s.id, symbol)

    with ctx.use_scope(symbol.scope):
        for attr_id, attr_symbol in symbol.attrs:
            if issubclass(type(attr_symbol), AttrFunSym):
                hoist_expr(ctx, attr_symbol.ast.type)

                for param in attr_symbol.ast.param_ids:
                    attr_symbol.scope.insert(param, VarSym())

                if attr_symbol.ast.body is not None:
                    with ctx.use_scope(attr_symbol.scope):
                        hoist_block(ctx, attr_symbol.ast.body)

            elif type(attr_symbol) is FunSym:
                hoist_fun(ctx, attr_symbol.ast)

            elif type(attr_symbol) is DataAttrSym:
                pass

            else:
                raise Todo(attr_symbol)


def hoist_fun(ctx, f):
    symbol = FunSym(
        ctx.unit,
        ctx.scope,
        f.type,
        f.id,
        f.param_ids,
        f.body,
        is_vargs = f.is_vargs,
        is_cfun = f.is_cfun,
        is_attr = f.is_attr
    )

    ctx.scope.insert(f.id, symbol)

    hoist_expr(ctx, f.type)

    for param in symbol.param_ids:
        symbol.scope.insert(param, VarSym())

    if symbol.body is not None:
        with ctx.use_scope(symbol.scope):
            hoist_block(ctx, symbol.body)

def hoist_fun_type(ctx, fun_type):
    hoist_expr(ctx, fun_type.ret_type)

    for param in fun_type.param_types:
        hoist_expr(ctx, param)

def hoist_if_statement(ctx, statement):
    ctx.set_scope(statement, Scope(ctx.scope))

    with ctx.use_scope(ctx.get_scope(statement)):
        for condition, block in statement.if_branches:
            hoist_expr(ctx, condition)
            hoist_block(ctx, block)

        if statement.else_block is not None:
            hoist_block(ctx, statement.else_block)

def hoist_loop_statement(ctx, statement):
    ctx.set_scope(statement, Scope(ctx.scope))

    with ctx.use_scope(ctx.get_scope(statement)):
        if statement.for_clause is not None:
            hoist_expr(ctx, statement.for_clause)

        if statement.each_clause is not None:
            hoist_expr(ctx, statement.each_clause)

        if statement.while_clause is not None:
            hoist_expr(ctx, statement.while_clause)

        if statement.loop_body is not None:
            hoist_block(ctx, statement.loop_body)

        if statement.then_clause is not None:
            hoist_expr(ctx, statement.then_clause)

        if statement.until_clause is not None:
            hoist_expr(ctx, statement.until_clause)

def hoist_switch_statement(ctx, statement):
    ctx.set_scope(statement, Scope(ctx.scope))

    with ctx.use_scope(ctx.get_scope(statement)):
        for case_values, case_block in statement.case_branches:
            for value in case_values:
                hoist_expr(ctx, value)

            hoist_block(ctx, case_block)

        if statement.default_block is not None:
            hoist_block(ctx, statement.default_block)


def hoist_return_statement(ctx, statement):
    if statement.expr is not None:
        hoist_expr(ctx, statement.expr)

def hoist_try_statement(ctx, statement):
    hoist_block(ctx, statement.try_block)

    for clause in statement.catch_clauses:
        ctx.set_scope(clause, Scope(ctx.scope))

        with ctx.use_scope(ctx.get_scope(clause)):
            hoist_expr(ctx, clause.type)

            ctx.scope.insert(clause.id, VarSym())

            hoist_block(ctx, clause.block)

    if statement.default_catch is not None:
        hoist_block(ctx, statement.default_catch)
