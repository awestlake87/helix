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

    if issubclass(statement_type, ExprInfo):
        return gen_expr_deps(ctx, statement_info)

    elif statement_type is ReturnInfo:
        return gen_return_deps(ctx, statement_info)

    else:
        raise Todo(statement_type)

def gen_expr_deps(ctx, expr_info):
    expr_type = type(expr_info)

    if expr_type is FunInfo:
        return gen_fun_deps(ctx, expr_info)

    elif expr_type is FunTypeInfo:
        return gen_fun_type_deps(ctx, expr_info)

    elif expr_type is IntTypeInfo:
        return [ ]

    elif expr_type is AutoIntInfo:
        return [ ]

    elif expr_type is CallExprInfo:
        return gen_call_deps(ctx, expr_info)

    elif expr_type is SymbolInfo:
        return [ ]

    else:
        raise Todo(expr_type)

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
