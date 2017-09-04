from contextlib import contextmanager

from ..sym import *
from ..err import Todo

from .exprs import *
from .statements import *
from .types import *
from .values import *

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

    elif statement_type is IfSym:
        return gen_if_info(ctx, statement_sym)

    elif statement_type is LoopSym:
        return gen_loop_info(ctx, statement_sym)

    elif statement_type is SwitchSym:
        return gen_switch_info(ctx, statement_sym)

    elif issubclass(statement_type, ExprSym):
        return gen_expr_info(ctx, statement_sym)

    else:
        raise Todo(statement_type)

def gen_expr_info(ctx, expr_sym):
    expr_type = type(expr_sym)

    if expr_type is CallExprSym:
        return gen_call_expr_info(ctx, expr_sym)

    elif expr_type is InitExprSym:
        return gen_init_info(ctx, expr_sym)

    elif issubclass(expr_type, BinaryExprSym):
        return gen_binary_expr_info(ctx, expr_sym)

    elif issubclass(expr_type, UnaryExprSym):
        return gen_unary_expr_info(ctx, expr_sym)

    elif expr_type is FunSym:
        return gen_fun_info(ctx, expr_sym)

    elif expr_type is SymbolSym:
        return SymbolInfo(expr_sym.id)

    elif expr_type is AutoIntSym:
        return AutoIntInfo(expr_sym.value, expr_sym.radix)

    elif expr_type is IntSym:
        return IntInfo(
            expr_sym.num_bits,
            expr_sym.is_signed,
            expr_sym.value,
            expr_sym.radix
        )

    elif expr_type is FunTypeSym:
        return gen_fun_type_info(ctx, expr_sym)

    elif expr_type is IntTypeSym:
        return gen_int_type_info(ctx, expr_sym)

    else:
        raise Todo(expr_type)

def gen_binary_expr_info(ctx, expr_sym):
    expr_type = type(expr_sym)

    lhs = gen_expr_info(ctx, expr_sym.lhs)
    rhs = gen_expr_info(ctx, expr_sym.rhs)

    if expr_type is LtnSym:
        return LtnInfo(lhs, rhs)

    elif expr_type is GtnSym:
        return GtnInfo(lhs, rhs)

    elif expr_type is LeqSym:
        return LeqInfo(lhs, rhs)

    elif expr_type is GeqSym:
        return GeqInfo(lhs, rhs)

    elif expr_type is EqlSym:
        return EqlInfo(lhs, rhs)

    elif expr_type is NeqSym:
        return NeqInfo(lhs, rhs)

    elif expr_type is AssignSym:
        return AssignInfo(lhs, rhs)

    else:
        raise Todo(expr_type)

def gen_unary_expr_info(ctx, expr_sym):
    expr_type = type(expr_sym)

    operand = gen_expr_info(ctx, expr_sym.operand)

    if expr_type is PreIncExprSym:
        return PreIncInfo(operand)

    elif expr_type is PostIncExprSym:
        return PostIncInfo(operand)

    elif expr_type is PreDecExprSym:
        return PreDecInfo(operand)

    elif expr_type is PostDecExprSym:
        return PostDecInfo(operand)

    else:
        raise Todo(expr_type)

def gen_init_info(ctx, init_sym):
    lhs_type = type(init_sym.lhs)

    if lhs_type is SymbolSym:
        lhs = VarInfo()
        rhs = gen_expr_info(ctx, init_sym.rhs)

        ctx.scope.insert(init_sym.lhs.id, lhs)

        return InitInfo(lhs, rhs)

    else:
        raise Todo(lhs_type)

def gen_return_info(ctx, return_sym):
    return ReturnInfo(gen_expr_info(ctx, return_sym.expr))

def gen_if_info(ctx, if_sym):
    if_info = IfInfo(ctx.scope)

    with ctx.use_scope(if_info.scope):
        for condition, block in if_sym.if_branches:
            if_info.if_branches.append(
                (gen_expr_info(ctx, condition), gen_block_info(ctx, block))
            )

        if if_sym.else_block is not None:
            if_info.else_block = gen_block_info(ctx, if_sym.else_block)

    return if_info

def gen_loop_info(ctx, loop_sym):
    loop_info = LoopInfo(ctx.scope)

    with ctx.use_scope(loop_info.scope):
        if loop_sym.for_clause is not None:
            loop_info.for_clause = gen_expr_info(ctx, loop_sym.for_clause)

        if loop_sym.each_clause is not None:
            loop_info.each_clause = gen_expr_info(ctx, loop_sym.each_clause)

        if loop_sym.while_clause is not None:
            loop_info.while_clause = gen_expr_info(ctx, loop_sym.while_clause)

        if loop_sym.loop_body is not None:
            loop_info.loop_body = gen_block_info(ctx, loop_sym.loop_body)

        if loop_sym.then_clause is not None:
            loop_info.then_clause = gen_expr_info(ctx, loop_sym.then_clause)

        if loop_sym.until_clause is not None:
            loop_info.until_clause = gen_expr_info(ctx, loop_sym.until_clause)

    return loop_info

def gen_switch_info(ctx, switch_sym):
    switch_info = SwitchInfo(ctx.scope)

    switch_info.value = gen_expr_info(ctx, switch_sym.value)

    with ctx.use_scope(switch_info.scope):
        for case_values, case_block in switch_sym.case_branches:
            case_value_syms = [ ]

            for value in case_values:
                case_value_syms.append(gen_expr_info(ctx, value))

            switch_info.case_branches.append(
                (case_value_syms, gen_block_info(ctx, case_block))
            )

        if switch_sym.default_block is not None:
            switch_info.default_block = gen_block_info(
                ctx, switch_sym.default_block
            )

    return switch_info

def gen_call_expr_info(ctx, call_expr_sym):
    return CallInfo(
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
