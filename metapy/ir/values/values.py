
from ...err import NoImplicitCast

from llvmlite import ir

from ..symbols import SymbolTable
from ..types import NilType

class Value:
    def is_type(self):
        return False

    def is_rval(self):
        return False

    def is_lval(self):
        return False

    def get_llvm_rval(self, builder):
        raise NotApplicable()

    def get_llvm_lval(self, builder):
        raise NotApplicable()

    def as_type(self, other_type, builder):
        if self.type.can_convert_to(other_type):
            return self
        else:
            raise NoImplicitCast()

class Module(Value):
    pass

class Unit(Value):
    def __init__(self):
        self._module = ir.Module("todo")
        self.symbols = SymbolTable()

class NilValue(Value):
    def __init__(self, type=NilType()):
        self.type = type

    def as_type(self, other_type, builder):
        if self.type.can_convert_to(other_type):
            return NilValue(other_type)
        else:
            raise NoImplicitCast()

    def is_rval(self):
        return True

    def get_llvm_rval(self, builder):
        return ir.IntType(32)(0).inttoptr(self.type.get_llvm_type(builder))

class StaticValue(Value):
    def __init__(self, type, value):
        self.type = type
        self._value = value

    def as_type(self, other_type, builder):
        if self.type.can_convert_to(other_type):
            return StaticValue(other_type, self._value)
        else:
            raise NoImplicitCast()

    def is_rval(self):
        return True

    def get_llvm_rval(self, builder):
        return self.type.get_llvm_type(builder)(self._value)

class LlvmRhsValue(Value):
    def __init__(self, type, llvm_value):
        self.type = type
        self._value = llvm_value

    def is_rval(self):
        return True

    def get_llvm_rval(self, builder):
        return self._value
