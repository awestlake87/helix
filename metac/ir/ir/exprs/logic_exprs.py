
from ...err import ReturnTypeMismatch, NotApplicable, Todo
from ..symbols import SymbolTable
from ..values.values import (
    Value, ConstLlvmValue, StaticValue, FunLlvmRVal
)
from ..types import *

from .cmp_exprs import *

from llvmlite import ir

def gen_fun_as_bit(fun, value):
    if type(value) is NilValue:
        return StaticValue(IntType(1, False), 0)

    elif type(value.type) is IntType:
        return gen_fun_neq(fun, value, StaticValue(value.type, 0))

    else:
        raise Todo()
