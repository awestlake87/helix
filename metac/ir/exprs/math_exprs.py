from ..types import *

from .assign_exprs import gen_assign_code
from .ptr_exprs import gen_ptr_add_ir
from .cast_exprs import (
    get_common_type, get_concrete_type, gen_implicit_cast_ir
)

def gen_neg_ir(ctx, operand):
    t = get_concrete_type(operand.type)

    if type(t) is IntType:
        return LlvmValue(
            t,
            ctx.builder.neg(
                gen_implicit_cast_ir(ctx, operand, t).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_add_ir(ctx, lhs, rhs):
    if (
        type(lhs.type) is PtrType and (
            type(rhs.type) is IntType or type(rhs.type) is AutoIntType
        )
    ):
        return gen_ptr_add_ir(ctx, lhs, rhs)

    elif (
        type(rhs.type) is PtrType and (
            type(lhs.type) is IntType or type(lhs.type) is AutoIntType
        )
    ):
        return gen_ptr_add_ir(ctx, rhs, lhs)

    else:
        common_type = get_concrete_type(get_common_type(lhs.type, rhs.type))

        if type(common_type) is IntType:
            return LlvmValue(
                common_type,
                ctx.builder.add(
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

def gen_sub_ir(ctx, lhs, rhs):
    if (
        type(lhs.type) is PtrType and (
            type(rhs.type) is IntType or type(rhs.type) is AutoIntType
        )
    ):
        return gen_ptr_add_ir(ctx, lhs, gen_neg_ir(ctx, rhs))

    elif (
        type(rhs.type) is PtrType and (
            type(lhs.type) is IntType or type(lhs.type) is AutoIntType
        )
    ):
        return gen_ptr_add_ir(ctx, rhs, gen_neg_ir(ctx, lhs))

    else:
        common_type = get_concrete_type(get_common_type(lhs.type, rhs.type))

        if type(common_type) is IntType:
            return LlvmValue(
                common_type,
                ctx.builder.sub(
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

def gen_mul_ir(ctx, lhs, rhs):
    common_type = get_concrete_type(get_common_type(lhs.type, rhs.type))

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.mul(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_div_ir(ctx, lhs, rhs):
    common_type = get_concrete_type(get_common_type(lhs.type, rhs.type))

    if type(common_type) is IntType:
        if common_type.is_signed:
            return LlvmValue(
                common_type,
                ctx.builder.sdiv(
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
                ctx.builder.udiv(
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

def gen_mod_ir(ctx, lhs, rhs):
    common_type = get_concrete_type(get_common_type(lhs.type, rhs.type))

    if type(common_type) is IntType:
        if common_type.is_signed:
            return LlvmValue(
                common_type,
                ctx.builder.srem(
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
                ctx.builder.urem(
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

def gen_pre_inc_ir(ctx, operand):
    if type(operand.type) is IntType:
        gen_assign_code(
            ctx,
            operand,
            gen_add_ir(ctx, operand, IntValue(operand.type, 1))
        )
        return operand

    else:
        raise Todo()

def gen_post_inc_ir(ctx, operand):
    if type(operand.type) is IntType:
        value = LlvmValue(operand.type, operand.get_llvm_value())

        gen_assign_code(
            ctx,
            operand,
            gen_add_ir(ctx, operand, IntValue(operand.type, 1))
        )

        return value

    else:
        raise Todo()

def gen_pre_dec_ir(ctx, operand):
    if type(operand.type) is IntType:
        gen_assign_code(
            ctx,
            operand,
            gen_sub_ir(ctx, operand, IntValue(operand.type, 1))
        )
        return operand

    else:
        raise Todo()

def gen_post_dec_ir(ctx, operand):
    if type(operand.type) is IntType:
        value = LlvmValue(operand.type, operand.get_llvm_value())

        gen_assign_code(
            ctx,
            operand,
            gen_sub_ir(ctx, operand, IntValue(operand.type, 1))
        )

        return value

    else:
        raise Todo()
