from contextlib import contextmanager

from ..info import *
from ..err import Todo

def gen_unit_target(unit_info):
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

    jit_fun = FunInfo(
        unit_info,
        unit_info.scope,
        "__jit__",
        FunTypeInfo(IntTypeInfo(32, True), [ ]),
        [ ],
        is_cfun = True
    )
    jit_fun.body = unit_info.block

    unit_info.target.deps.append(jit_fun.target)

    ctx = Context(unit_info)

    with ctx.use_scope(unit_info.scope):
        jit_fun.target.deps += gen_block_deps(ctx, unit_info.block)

    return unit_info.target

def gen_block_deps(ctx, block_info):
    deps = [ ]

    with ctx.use_scope(block_info.scope):
        for statement in block_info.statements:
            deps += gen_statement_deps(ctx, statement)

    return deps

def gen_statement_deps(ctx, statement_info):
    statement_type = type(statement_info)

    if statement_type is ReturnInfo:
        return gen_return_deps(ctx, statement_info)

    elif statement_type is IfInfo:
        return gen_if_deps(ctx, statement_info)

    elif statement_type is LoopInfo:
        return gen_loop_deps(ctx, statement_info)

    elif statement_type is SwitchInfo:
        return gen_switch_deps(ctx, statement_info)

    elif issubclass(statement_type, ExprInfo):
        return gen_expr_deps(ctx, statement_info)

    else:
        raise Todo(statement_type)

def gen_expr_deps(ctx, expr_info):
    expr_type = type(expr_info)

    if expr_type is InitInfo:
        return gen_init_deps(ctx, expr_info)

    elif expr_type is CallInfo:
        return gen_call_deps(ctx, expr_info)

    elif issubclass(expr_type, BinaryExprInfo):
        return gen_binary_expr_deps(ctx, expr_info)

    elif issubclass(expr_type, UnaryExprInfo):
        return gen_unary_expr_deps(ctx, expr_info)

    elif expr_type is FunInfo:
        return gen_fun_deps(ctx, expr_info)

    elif expr_type is AutoIntInfo:
        return [ ]

    elif expr_type is IntInfo:
        return [ ]

    elif expr_type is SymbolInfo:
        return [ ]

    elif expr_type is FunTypeInfo:
        return gen_fun_type_deps(ctx, expr_info)

    elif expr_type is IntTypeInfo:
        return [ ]

    else:
        raise Todo(expr_type)

def gen_binary_expr_deps(ctx, expr_info):
    return (
        gen_expr_deps(ctx, expr_info.lhs) + gen_expr_deps(ctx, expr_info.rhs)
    )

def gen_unary_expr_deps(ctx, expr_info):
    return gen_expr_deps(ctx, expr_info.operand)

def gen_fun_deps(ctx, fun_info):
    fun_info.proto_target.deps += gen_expr_deps(ctx, fun_info.type)

    with ctx.use_scope(fun_info.scope):
        fun_info.target.deps += gen_block_deps(ctx, fun_info.body)

    return [ ]

def gen_fun_type_deps(ctx, fun_type_info):
    deps = gen_expr_deps(ctx, fun_type_info.ret_type)

    for param_type in fun_type_info.param_types:
        deps += gen_expr_deps(ctx, param_type)

    return deps

def gen_init_deps(ctx, expr_info):
    return gen_expr_deps(ctx, expr_info.rhs)

def gen_call_deps(ctx, call_info):
    deps = gen_expr_deps(ctx, call_info.lhs)

    lhs_type = type(call_info.lhs)

    if lhs_type is SymbolInfo:
        fun_info = ctx.scope.resolve(call_info.lhs.id)

        deps.append(fun_info.proto_target)
        ctx.unit.target.deps.append(fun_info.target)

    else:
        raise Todo(lhs_type)

    for arg_info in call_info.args:
        deps += gen_expr_deps(ctx, arg_info)

    return deps


def gen_return_deps(ctx, return_info):
    if return_info.expr is not None:
        return gen_expr_deps(ctx, return_info.expr)

    else:
        return [ ]

def gen_if_deps(ctx, if_info):
    deps = [ ]

    with ctx.use_scope(if_info.scope):
        for condition, block in if_info.if_branches:
            deps += gen_expr_deps(ctx, condition)
            deps += gen_block_deps(ctx, block)

        if if_info.else_block is not None:
            deps += gen_block_deps(ctx, if_info.else_block)

    return deps

def gen_loop_deps(ctx, loop_info):
    deps = [ ]

    with ctx.use_scope(loop_info.scope):
        if loop_info.for_clause is not None:
            deps += gen_expr_deps(ctx, loop_info.for_clause)

        if loop_info.each_clause is not None:
            deps += gen_expr_deps(ctx, loop_info.each_clause)

        if loop_info.while_clause is not None:
            deps += gen_expr_deps(ctx, loop_info.while_clause)

        if loop_info.loop_body is not None:
            deps += gen_block_deps(ctx, loop_info.loop_body)

        if loop_info.then_clause is not None:
            deps += gen_expr_deps(ctx, loop_info.then_clause)

        if loop_info.until_clause is not None:
            deps += gen_expr_deps(ctx, loop_info.until_clause)

    return deps

def gen_switch_deps(ctx, switch_info):
    deps = [ ]

    with ctx.use_scope(switch_info.scope):
        for case_values, case_block in switch_info.case_branches:
            for value in case_values:
                deps += gen_expr_deps(ctx, value)
            deps += gen_block_deps(ctx, case_block)

        if switch_info.default_block is not None:
            deps += gen_block_deps(ctx, switch_info.default_block)

    return deps
