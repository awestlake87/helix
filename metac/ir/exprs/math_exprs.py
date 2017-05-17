from ...err import Todo, CompilerBug
from ..values.values import *
from ..types import *

from llvmlite import ir

from .misc_exprs import gen_fun_assign, gen_fun_as

def gen_fun_neg(fun, operand):
    op_type = get_concrete_type(operand.type)

    if type(op_type) is IntType:
        return FunLlvmRVal(
            fun,
            op_type,
            fun._builder.neg(
                gen_fun_as(fun, operand, op_type).get_llvm_rval()
            )
        )

    else:
        raise Todo()

def gen_fun_add(fun, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return FunLlvmRVal(
            fun,
            common_type,
            fun._builder.add(
                gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                gen_fun_as(fun, rhs, common_type).get_llvm_rval()
            )
        )

    else:
        raise Todo()

def gen_fun_sub(fun, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return FunLlvmRVal(
            fun,
            common_type,
            fun._builder.sub(
                gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                gen_fun_as(fun, rhs, common_type).get_llvm_rval()
            )
        )

    else:
        raise Todo()

def gen_fun_mul(fun, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return FunLlvmRVal(
            fun,
            common_type,
            fun._builder.mul(
                gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                gen_fun_as(fun, rhs, common_type).get_llvm_rval()
            )
        )

    else:
        raise Todo()

def gen_fun_div(fun, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        if common_type._is_signed:
            return FunLlvmRVal(
                fun,
                common_type,
                fun._builder.sdiv(
                    gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                    gen_fun_as(fun, rhs, common_type).get_llvm_rval()
                )
            )
        else:
            return FunLlvmRVal(
                fun,
                common_type,
                fun._builder.udiv(
                    gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                    gen_fun_as(fun, rhs, common_type).get_llvm_rval()
                )
            )

    else:
        raise Todo()

def gen_fun_mod(fun, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        if common_type._is_signed:
            return FunLlvmRVal(
                fun,
                common_type,
                fun._builder.srem(
                    gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                    gen_fun_as(fun, rhs, common_type).get_llvm_rval()
                )
            )
        else:
            return FunLlvmRVal(
                fun,
                common_type,
                fun._builder.urem(
                    gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                    gen_fun_as(fun, rhs, common_type).get_llvm_rval()
                )
            )

    else:
        raise Todo()

def gen_fun_pre_inc(fun, operand):
    if not operand.is_lval():
        raise NotApplicable()

    op_type = get_concrete_type(operand.type)

    if type(op_type) is IntType:
        return gen_fun_assign(
            fun,
            operand,
            FunLlvmRVal(
                fun,
                op_type,
                fun._builder.add(
                    gen_fun_as(fun, operand, op_type).get_llvm_rval(),
                    StaticValue(op_type, 1).get_llvm_rval()
                )
            )
        )

    else:
        raise Todo()

def gen_fun_post_inc(fun, operand):
    if not operand.is_lval():
        raise NotApplicable()

    op_type = get_concrete_type(operand.type)

    if type(op_type) is IntType:
        value = FunLlvmRVal(
            fun,
            op_type,
            gen_fun_as(fun, operand, op_type).get_llvm_rval()
        )

        gen_fun_assign(
            fun,
            operand,
            FunLlvmRVal(
                fun,
                op_type,
                fun._builder.add(
                    value.get_llvm_rval(),
                    StaticValue(op_type, 1).get_llvm_rval()
                )
            )
        )

        return value

    else:
        raise Todo()

def gen_fun_pre_dec(fun, operand):
    if not operand.is_lval():
        raise NotApplicable()

    op_type = get_concrete_type(operand.type)

    if type(op_type) is IntType:
        return gen_fun_assign(
            fun,
            operand,
            FunLlvmRVal(
                fun,
                op_type,
                fun._builder.sub(
                    gen_fun_as(fun, operand, op_type).get_llvm_rval(),
                    StaticValue(op_type, 1).get_llvm_rval()
                )
            )
        )

    else:
        raise Todo()

def gen_fun_post_dec(fun, operand):
    if not operand.is_lval():
        raise NotApplicable()

    op_type = get_concrete_type(operand.type)

    if type(op_type) is IntType:
        value = FunLlvmRVal(
            fun,
            op_type,
            gen_fun_as(fun, operand, op_type).get_llvm_rval()
        )

        gen_fun_assign(
            fun,
            operand,
            FunLlvmRVal(
                fun,
                op_type,
                fun._builder.sub(
                    value.get_llvm_rval(),
                    StaticValue(op_type, 1).get_llvm_rval()
                )
            )
        )

        return value

    else:
        raise Todo()
