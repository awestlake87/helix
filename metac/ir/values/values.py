from contextlib import contextmanager

from ...err import NoImplicitCast, Todo, CompilerBug

from llvmlite import ir

from ..symbols import SymbolTable
from ..types import NilType, IntType, AutoIntType

class Value:
    def is_type(self):
        return False

    def is_lval(self):
        return False

    def is_rval(self):
        return False

    def is_static(self):
        return False

    def get_llvm_rval(self):
        raise NotApplicable()

class NilValue(Value):
    def __init__(self, type=NilType()):
        self.type = type

    def is_rval(self):
        return True

    def get_llvm_rval(self):
        return ir.IntType(32)(0).inttoptr(self.type.get_llvm_type())

class StaticValue(Value):
    def __init__(self, type, value):
        self.type = type
        self._value = value

    def is_static(self):
        return True

    def is_rval(self):
        return True

    def get_llvm_rval(self):
        return self.type.get_llvm_type()(self._value)


class LlvmValue(Value):
    def __init__(self, type, llvm_value):
        self.type = type
        self._value = llvm_value


class FunLlvmRVal(LlvmValue):
    def __init__(self, fun, type, llvm_value):
        super().__init__(type, llvm_value)
        self._fun = fun

    def is_rval(self):
        return True

    def get_llvm_rval(self):
        return self._value

class ConstLlvmValue(LlvmValue):
    def is_rval(self):
        return True

    def get_llvm_rval(self):
        return self._value

class StackValue(LlvmValue):
    def __init__(self, fun, type, value):
        super().__init__(type, value)

        self._fun = fun

    def is_lval(self):
        return True

    def get_llvm_rval(self):
        return self._fun._builder.load(self._value)

    def dot_access(self, id):
        raise Todo()
