from contextlib import contextmanager

from ..sym import *
from ..err import Todo

from .exprs import CallExprInfo
from .statements import BlockInfo, ReturnInfo
from .types import FunTypeInfo, IntTypeInfo
from .values import UnitInfo, FunInfo, VarInfo, AutoIntInfo, SymbolInfo

def gen_unit_info(unit_sym):
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

    unit_info = UnitInfo()
    ctx = Context(unit_info)

    with ctx.use_scope(unit_info.scope):
        unit_info.block = gen_block_info(ctx, unit_sym.block)

    return unit_info

def gen_block_info(ctx, block_sym):
    block_info = BlockInfo(ctx.scope)

    with ctx.use_scope(block_info.scope):
        for statement in block_sym.statements:
            block_info.statements.append(gen_statement_info(ctx, statement))

    return block_info

def gen_statement_info(ctx, statement_sym):
    statement_type = type(statement_sym)

    if statement_type is ReturnSym:
        return gen_return_info(ctx, statement_sym)

    elif issubclass(statement_type, ExprSym):
        return gen_expr_info(ctx, statement_sym)

    else:
        raise Todo(statement_type)

def gen_expr_info(ctx, expr_sym):
    expr_type = type(expr_sym)

    if expr_type is CallExprSym:
        return gen_call_expr_info(ctx, expr_sym)

    elif expr_type is FunSym:
        return gen_fun_info(ctx, expr_sym)

    elif expr_type is SymbolSym:
        return SymbolInfo(expr_sym.id)

    elif expr_type is AutoIntSym:
        return AutoIntInfo(expr_sym.value, expr_sym.radix)

    elif expr_type is FunTypeSym:
        return gen_fun_type_info(ctx, expr_sym)

    elif expr_type is IntTypeSym:
        return gen_int_type_info(ctx, expr_sym)

    else:
        raise Todo(expr_type)

def gen_return_info(ctx, return_sym):
    return ReturnInfo(gen_expr_info(ctx, return_sym.expr))

def gen_call_expr_info(ctx, call_expr_sym):
    return CallExprInfo(
        gen_expr_info(ctx, call_expr_sym.lhs),
        [ gen_expr_info(ctx, arg_sym) for arg_sym in call_expr_sym.args ]
    )

def gen_fun_info(ctx, fun_sym):
    fun_type_info = gen_expr_info(ctx, fun_sym.type)

    fun_info = FunInfo(
        ctx.unit,
        ctx.scope,
        fun_sym.id,
        fun_type_info,
        fun_sym.param_ids,
        is_cfun = fun_sym.is_cfun
    )
    ctx.scope.insert(fun_sym.id, fun_info)

    with ctx.use_scope(fun_info.scope):
        for param_id in fun_sym.param_ids:
            ctx.scope.insert(param_id, VarInfo())

        if fun_sym.body is not None:
            fun_info.body = gen_block_info(ctx, fun_sym.body)

    return fun_info

def gen_fun_type_info(ctx, fun_type_sym):
    return FunTypeInfo(
        gen_expr_info(ctx, fun_type_sym.ret_type),
        [
            gen_expr_info(ctx, param_sym)
            for param_sym in
            fun_type_sym.param_types
        ]
    )

def gen_int_type_info(ctx, int_type_sym):
    return IntTypeInfo(int_type_sym.num_bits, int_type_sym.is_signed)
