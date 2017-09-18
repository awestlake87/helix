from ..types import *

from .cast_exprs import (
    gen_as_bit_ir, get_concrete_type, get_common_type, gen_implicit_cast_ir
)

def gen_mut_ir(ctx, operand):
    return operand

def gen_ternary_conditional_ir(ctx, expr):
    from .exprs import gen_expr_ir

    tern_true = ctx.builder.append_basic_block("tern_true")
    tern_false = ctx.builder.append_basic_block("tern_false")
    tern_end = ctx.builder.append_basic_block("tern_end")

    ctx.builder.cbranch(
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.condition)).get_llvm_value(),
        tern_true,
        tern_false
    )

    lhs_value = None
    rhs_value = None

    with ctx.builder.goto_block(tern_true):
        lhs_value = gen_expr_ir(ctx, expr.lhs)
        ctx.builder.branch(tern_end)

    with ctx.builder.goto_block(tern_false):
        rhs_value = gen_expr_ir(ctx, expr.rhs)
        ctx.builder.branch(tern_end)

    val_type = get_concrete_type(
        get_common_type(lhs_value.type, rhs_value.type)
    )

    ctx.builder.position_at_start(tern_end)
    phi = ctx.builder.phi(val_type.get_llvm_value())

    phi.add_incoming(
        gen_implicit_cast_ir(ctx, lhs_value, val_type).get_llvm_value(),
        tern_true
    )
    phi.add_incoming(
        gen_implicit_cast_ir(ctx, rhs_value, val_type).get_llvm_value(),
        tern_false
    )

    return LlvmValue(val_type, phi)
