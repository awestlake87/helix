from ..types import *

from .cast_exprs import (
    gen_implicit_cast_ir, gen_as_bit_ir, get_common_type
)

def gen_and_ir(ctx, expr):
    from .exprs import gen_expr_ir

    and_lhs_true = ctx.builder.append_basic_block("and_lhs_true")
    and_true = ctx.builder.append_basic_block("and_true")
    and_false = ctx.builder.append_basic_block("and_false")
    and_end = ctx.builder.append_basic_block("and_end")

    ctx.builder.cbranch(
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.lhs)).get_llvm_value(),
        and_lhs_true,
        and_false
    )

    ctx.builder.position_at_start(and_end)
    phi = ctx.builder.phi(BitType().get_llvm_value())

    with ctx.builder.goto_block(and_lhs_true):
        ctx.builder.cbranch(
            gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.rhs)).get_llvm_value(),
            and_true,
            and_false
        )

    with ctx.builder.goto_block(and_true):
        phi.add_incoming(
            ir.IntType(1)(1),
            and_true
        )
        ctx.builder.branch(and_end)

    with ctx.builder.goto_block(and_false):
        phi.add_incoming(
            ir.IntType(1)(0),
            and_false
        )
        ctx.builder.branch(and_end)

    return LlvmValue(BitType(), phi)

def gen_or_ir(ctx, expr):
    from .exprs import gen_expr_ir

    or_lhs_false = ctx.builder.append_basic_block("or_lhs_false")
    or_true = ctx.builder.append_basic_block("or_true")
    or_false = ctx.builder.append_basic_block("or_false")
    or_end = ctx.builder.append_basic_block("or_end")

    ctx.builder.cbranch(
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.lhs)).get_llvm_value(),
        or_true,
        or_lhs_false
    )

    ctx.builder.position_at_start(or_end)
    phi = ctx.builder.phi(BitType().get_llvm_value())

    with ctx.builder.goto_block(or_lhs_false):
        ctx.builder.cbranch(
            gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.rhs)).get_llvm_value(),
            or_true,
            or_false
        )

    with ctx.builder.goto_block(or_true):
        phi.add_incoming(
            ir.IntType(1)(1),
            or_true
        )
        ctx.builder.branch(or_end)

    with ctx.builder.goto_block(or_false):
        phi.add_incoming(
            ir.IntType(1)(0),
            or_false
        )
        ctx.builder.branch(or_end)

    return LlvmValue(BitType(), phi)

def gen_not_ir(ctx, expr):
    from .exprs import gen_expr_ir
    from .bitwise_exprs import gen_bit_not_ir

    return gen_bit_not_ir(
        ctx,
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.operand))
    )

def gen_xor_ir(ctx, expr):
    from .exprs import gen_expr_ir
    from .bitwise_exprs import gen_bit_xor_ir

    return gen_bit_xor_ir(
        ctx,
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.lhs)),
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.rhs))
    )

def _gen_fun_cmp(ctx, op, lhs, rhs):
    cmp_type = get_common_type(lhs.type, rhs.type)

    if type(cmp_type) is IntType:
        if cmp_type.is_signed:
            return LlvmValue(
                BitType(),
                ctx.builder.icmp_signed(
                    op,
                    gen_implicit_cast_ir(ctx, lhs, cmp_type).get_llvm_value(),
                    gen_implicit_cast_ir(ctx, rhs, cmp_type).get_llvm_value()
                )
            )
        else:
            return LlvmValue(
                BitType(),
                ctx.builder.icmp_unsigned(
                    op,
                    gen_implicit_cast_ir(ctx, lhs, cmp_type).get_llvm_value(),
                    gen_implicit_cast_ir(ctx, rhs, cmp_type).get_llvm_value()
                )
            )
    elif type(cmp_type) is PtrType:
        return LlvmValue(
            BitType(),
            ctx.builder.icmp_unsigned(
                op,
                gen_implicit_cast_ir(ctx, lhs, cmp_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, cmp_type).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_ltn_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "<", lhs, rhs)

def gen_leq_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "<=", lhs, rhs)

def gen_gtn_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, ">", lhs, rhs)

def gen_geq_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, ">=", lhs, rhs)

def gen_eql_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "==", lhs, rhs)

def gen_neq_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "!=", lhs, rhs)
