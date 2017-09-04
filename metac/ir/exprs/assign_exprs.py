from ..types import *

from ...info import SymbolInfo, GlobalInfo

from .cast_exprs import gen_implicit_cast_ir, get_concrete_type

def gen_init_ir(ctx, expr):
    from .exprs import gen_expr_ir

    rhs = gen_expr_ir(ctx, expr.rhs)

    if type(expr.lhs) is SymbolInfo:
        lhs = StackValue(ctx, get_concrete_type(rhs.type))

        ctx.scope.resolve(expr.lhs.id).set_ir_value(lhs)

        gen_assign_code(ctx, lhs, rhs)

        return lhs

    elif type(expr.lhs) is GlobalInfo:
        lhs = gen_expr_ir(ctx, expr.lhs)

        gen_assign_code(ctx, lhs, rhs)

        return lhs

    else:
        raise Todo(expr)

def gen_assign_code(ctx, lhs, rhs):
    ctx.builder.store(
        gen_implicit_cast_ir(ctx, rhs, lhs.type).get_llvm_value(),
        lhs.get_llvm_ptr()
    )
