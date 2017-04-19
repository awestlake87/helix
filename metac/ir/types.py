
from ..err import Todo

from llvmlite import ir

class Type:
    def is_type(self):
        return True

    def can_convert_to(self, other_type):
        return False

class PtrType(Type):
    def __init__(self, type):
        self._type = type

    def get_llvm_type(self, builder):
        return self._type.get_llvm_type(builder).as_pointer()

class NilType(Type):
    def can_convert_to(self, other):
        if type(other) is PtrType:
            return True
        else:
            return False

    def get_llvm_type(self, builder):
        return ir.IntType(64)

class IntType(Type):
    def __init__(self, num_bits=32, is_signed=True):
        self._num_bits = num_bits
        self._is_signed = is_signed

    def can_convert_to(self, other):
        if type(other) is IntType and self._num_bits == other._num_bits:
            if self._is_signed and other._is_signed:
                return True
            elif not self._is_signed and not other._is_signed:
                return True
            else:
                return False
        else:
            return False

    def get_llvm_type(self, builder):
        return ir.IntType(self._num_bits)

    def call(self, fun, args):
        if len(args) != 1:
            raise Todo("invalid args")

        if args[0].type.can_convert_to(self):
            return args[0].as_type(self, fun._builder)
        else:
            raise Todo("invalid args")


class AutoIntType(Type):
    def can_convert_to(self, other):
        if type(other) is IntType:
            return True
        else:
            return False

class FunType(Type):
    def __init__(self, ret_type, param_types):
        self._ret_type = ret_type
        self._param_types = param_types

    def get_llvm_type(self, builder):
        return ir.FunctionType(
            self._ret_type.get_llvm_type(builder),
            [ t.get_llvm_type(builder) for t in self._param_types ]
        )
