from ...err import ReturnTypeMismatch
from ..values.values import *
from ..types import *

from llvmlite import ir

from ..exprs import gen_fun_as

def gen_fun_return(fun, value):
    if value.type.can_convert_to(fun.type._ret_type):
        ret_value = gen_fun_as(fun, value, fun.type._ret_type)
        fun._builder.ret(ret_value.get_llvm_rval())

    else:
        raise ReturnTypeMismatch()
