from contextlib import contextmanager

from ..ast import *
from ..err import Todo

from .exprs import CallExprSym
from .statements import BlockSym, ReturnSym
from .types import FunTypeSym, IntTypeSym
from .values import UnitSym, FunSym, VarSym, AutoIntSym, SymbolSym

def gen_unit_sym(unit_node):
    class Context:
        def __init__(self, unit):
            self.unit = unit
            self.scope = None

        @contextmanager
        def use_scope(self, scope):
            old_scope = self.scope
            self.scope = scope

            yield

            self.scope = old_scope

    unit_sym = UnitSym()
    ctx = Context(unit_sym)

    with ctx.use_scope(unit_sym.scope):
        unit_sym.block = gen_block_sym(ctx, unit_node)

    return unit_sym

def gen_block_sym(ctx, block_node):
    block_sym = BlockSym(ctx.scope)

    with ctx.use_scope(block_sym.scope):
        for statement in block_node.statements:
            block_sym.statements.append(gen_statement_sym(ctx, statement))

    return block_sym

def gen_statement_sym(ctx, statement_node):
    statement_type = type(statement_node)

    if statement_type is ReturnNode:
        return gen_return_sym(ctx, statement_node)

    elif issubclass(statement_type, ExprNode):
        return gen_expr_sym(ctx, statement_node)

    else:
        raise Todo(statement_type)

def gen_expr_sym(ctx, expr_node):
    expr_type = type(expr_node)

    if expr_type is CallExprNode:
        return gen_call_expr_sym(ctx, expr_node)

    elif expr_type is FunNode:
        return gen_fun_sym(ctx, expr_node)

    elif expr_type is SymbolNode:
        return SymbolSym(expr_node.id)

    elif expr_type is AutoIntNode:
        return AutoIntSym(expr_node.value, expr_node.radix)

    elif expr_type is FunTypeNode:
        return gen_fun_type_sym(ctx, expr_node)

    elif expr_type is IntTypeNode:
        return gen_int_type_sym(ctx, expr_node)

    else:
        raise Todo(expr_type)

def gen_return_sym(ctx, return_node):
    return ReturnSym(gen_expr_sym(ctx, return_node.expr))

def gen_call_expr_sym(ctx, call_expr_node):
    return CallExprSym(
        gen_expr_sym(ctx, call_expr_node.lhs),
        [ gen_expr_sym(ctx, arg_node) for arg_node in call_expr_node.args ]
    )

def gen_fun_sym(ctx, fun_node):
    fun_type_sym = gen_expr_sym(ctx, fun_node.type)

    fun_sym = FunSym(
        ctx.scope,
        fun_node.id,
        fun_type_sym,
        fun_node.param_ids,
        is_cfun = fun_node.is_cfun
    )
    ctx.scope.insert(fun_node.id, fun_sym)

    with ctx.use_scope(fun_sym.scope):
        for param_id in fun_node.param_ids:
            ctx.scope.insert(param_id, VarSym())

        if fun_node.body is not None:
            fun_sym.body = gen_block_sym(ctx, fun_node.body)

    return fun_sym

def gen_fun_type_sym(ctx, fun_type_node):
    return FunTypeSym(
        gen_expr_sym(ctx, fun_type_node.ret_type),
        [
            gen_expr_sym(ctx, param_node)
            for param_node in
            fun_type_node.param_types
        ]
    )

def gen_int_type_sym(ctx, int_type_node):
    return IntTypeSym(int_type_node.num_bits, int_type_node.is_signed)
