from ...err import Todo, CompilerBug
from ..values.values import *
from ..types import *

from llvmlite import ir

from .misc_exprs import gen_fun_as

def gen_fun_bit_and(fun, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return FunLlvmRVal(
            fun,
            common_type,
            fun._builder.and_(
                gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                gen_fun_as(fun, rhs, common_type).get_llvm_rval()
            )
        )

    else:
        raise Todo()

def gen_fun_bit_xor(fun, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return FunLlvmRVal(
            fun,
            common_type,
            fun._builder.xor(
                gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                gen_fun_as(fun, rhs, common_type).get_llvm_rval()
            )
        )

    else:
        raise Todo()

def gen_fun_bit_or(fun, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return FunLlvmRVal(
            fun,
            common_type,
            fun._builder.or_(
                gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                gen_fun_as(fun, rhs, common_type).get_llvm_rval()
            )
        )

    else:
        raise Todo()

def gen_fun_bit_not(fun, operand):
    common_type = get_concrete_type(operand.type)

    if type(common_type) is IntType:
        return FunLlvmRVal(
            fun,
            common_type,
            fun._builder.not_(
                gen_fun_as(fun, operand, common_type).get_llvm_rval()
            )
        )

    else:
        raise Todo()

def gen_fun_bit_shr(fun, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        if common_type._is_signed:
            return FunLlvmRVal(
                fun,
                common_type,
                fun._builder.ashr(
                    gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                    gen_fun_as(fun, rhs, common_type).get_llvm_rval()
                )
            )
        else:
            return FunLlvmRVal(
                fun,
                common_type,
                fun._builder.lshr(
                    gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                    gen_fun_as(fun, rhs, common_type).get_llvm_rval()
                )
            )

    else:
        raise Todo()

def gen_fun_bit_shl(fun, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return FunLlvmRVal(
            fun,
            common_type,
            fun._builder.shl(
                gen_fun_as(fun, lhs, common_type).get_llvm_rval(),
                gen_fun_as(fun, rhs, common_type).get_llvm_rval()
            )
        )

    else:
        raise Todo()
