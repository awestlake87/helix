
from ...err import NoImplicitCast, Todo, CompilerBug

from llvmlite import ir

from ..symbols import SymbolTable
from ..types import NilType

class Value:
    def is_type(self):
        return False

    def is_rval(self):
        return False

    def is_static(self):
        return False

    def get_llvm_rval(self, builder):
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

    def is_static(self):
        return True

    def is_rval(self):
        return True

    def get_llvm_rval(self, builder):
        return self.type.get_llvm_type(builder)(self._value)


class LlvmValue(Value):
    def __init__(self, type, llvm_value):
        self.type = type
        self._value = llvm_value


class ConstLlvmValue(LlvmValue):
    def is_rval(self):
        return True

    def get_llvm_rval(self, builder):
        return self._value

class StackValue(LlvmValue):
    def __init__(self, fun, type, value):
        super().__init__(type, value)

        self._fun = fun

    def get_llvm_rval(self, builder):
        return builder.load(self._value)

    def initialize(self, value):
        if not value.type.can_convert_to(self.type):
            raise CompilerBug("type mismatch in function level init")

        actual_value = value.as_type(self.type, self._fun._builder)

        self._fun._builder.store(
            actual_value.get_llvm_rval(self._fun._builder), self._value
        )
        return self
