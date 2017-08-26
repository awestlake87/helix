from ..types import *

from .cast_exprs import (
    gen_implicit_cast_ir, get_common_type, get_concrete_type
)

def gen_bit_and_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.and_(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_bit_or_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.or_(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_bit_not_ir(ctx, operand):
    common_type = get_concrete_type(operand.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.not_(
                gen_implicit_cast_ir(
                    ctx, operand, common_type
                ).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_bit_xor_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.xor(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_bit_shr_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        if common_type.is_signed:
            return LlvmValue(
                common_type,
                ctx.builder.ashr(
                    gen_implicit_cast_ir(
                        ctx, lhs, common_type
                    ).get_llvm_value(),
                    gen_implicit_cast_ir(
                        ctx, rhs, common_type
                    ).get_llvm_value()
                )
            )
        else:
            return LlvmValue(
                common_type,
                ctx.builder.lshr(
                    gen_implicit_cast_ir(
                        ctx, lhs, common_type
                    ).get_llvm_value(),
                    gen_implicit_cast_ir(
                        ctx, rhs, common_type
                    ).get_llvm_value()
                )
            )

    else:
        raise Todo()

def gen_bit_shl_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.shl(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()
