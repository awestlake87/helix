
from ...err import ReturnTypeMismatch, NotApplicable, Todo
from ..symbols import SymbolTable
from ..values.values import (
    Value, ConstLlvmValue, StaticValue, FunLlvmRVal
)
from ..types import *

from .misc_exprs import *

from llvmlite import ir

def _gen_fun_cmp(fun, op, lhs, rhs):
    cmp_type = get_common_type(lhs.type, rhs.type)

    if type(cmp_type) is IntType:
        if cmp_type._is_signed:
            return FunLlvmRVal(
                fun,
                IntType(1, False),
                fun._builder.icmp_signed(
                    op,
                    gen_fun_as(fun, lhs, cmp_type).get_llvm_rval(),
                    gen_fun_as(fun, rhs, cmp_type).get_llvm_rval()
                )
            )
        else:
            return FunLlvmRVal(
                fun,
                IntType(1, False),
                fun._builder.icmp_unsigned(
                    op,
                    gen_fun_as(fun, lhs, cmp_type).get_llvm_rval(),
                    gen_fun_as(fun, rhs, cmp_type).get_llvm_rval()
                )
            )
    else:
        raise Todo()



def gen_fun_ltn(fun, lhs, rhs):
    return _gen_fun_cmp(fun, "<", lhs, rhs)

def gen_fun_leq(fun, lhs, rhs):
    return _gen_fun_cmp(fun, "<=", lhs, rhs)

def gen_fun_gtn(fun, lhs, rhs):
    return _gen_fun_cmp(fun, ">", lhs, rhs)

def gen_fun_geq(fun, lhs, rhs):
    return _gen_fun_cmp(fun, ">=", lhs, rhs)

def gen_fun_eql(fun, lhs, rhs):
    return _gen_fun_cmp(fun, "==", lhs, rhs)

def gen_fun_neq(fun, lhs, rhs):
    return _gen_fun_cmp(fun, "!=", lhs, rhs)
