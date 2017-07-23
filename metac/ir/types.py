
from ..err import Todo

from llvmlite import ir

class Type:
    def is_type(self):
        return True

    def is_equal_to(self, other_type):
        return False

    def can_convert_to(self, other_type):
        return False

class PtrType(Type):
    def __init__(self, type):
        self._type = type

    def is_equal_to(self, other_type):
        raise Todo()

    def get_llvm_type(self):
        return self._type.get_llvm_type().as_pointer()

class NilType(Type):
    def can_convert_to(self, other):
        if type(other) is PtrType:
            return True
        else:
            return False

    def is_equal_to(self, other_type):
        if type(other_type) is NilType:
            return True
        else:
            return False

    def get_llvm_type(self):
        return ir.IntType(64)

class IntType(Type):
    def __init__(self, num_bits=32, is_signed=True):
        self._num_bits = num_bits
        self._is_signed = is_signed

    def is_equal_to(self, other_type):
        if self.can_convert_to(other_type):
            return True
        else:
            return False

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

    def get_llvm_type(self):
        return ir.IntType(self._num_bits)


class AutoIntType(Type):

    def is_equal_to(self, other_type):
        if type(other_type) is AutoIntType:
            return True
        else:
            return False

    def can_convert_to(self, other):
        if type(other) is IntType:
            return True
        else:
            return False

class FunType(Type):
    def __init__(self, ret_type, param_types):
        self._ret_type = ret_type
        self._param_types = param_types

    def is_equal_to(self, other_type):
        raise Todo()

    def get_llvm_type(self):
        return ir.FunctionType(
            self._ret_type.get_llvm_type(),
            [ t.get_llvm_type() for t in self._param_types ]
        )

class StructType(Type):
    def __init__(self, attrs=[]):
        self._attrs = attrs

    def is_equal_to(self, other_type):
        if type(other_type) is StructType:
            for a1, a2 in zip(self._attrs, other_type._attrs):
                t1, id1 = a1
                t2, id2 = a2

                if not t1.is_equal_to(t2) or id1 != id2:
                    return False

            return True

    def can_convert_to(self, other_type):
        return self.is_equal_to(other_type)

    def get_llvm_type(self):
        return ir.LiteralStructType(
            [ t.get_llvm_type() for t, id in self._attrs ]
        )

    def get_attr_info(self, id):
        for i in range(0, len(self._attrs)):
            attr_type, attr_id = self._attrs[i]

            if attr_id == id:
                return (attr_type, i)

        raise Todo(
            "make a \"unable to resolve struct attr '{}'\" error".format(id)
        )


def get_common_type(a, b):
    if type(a) is IntType and type(b) is IntType:
        if a._num_bits != b._num_bits:
            return None

        elif a._is_signed and not b._is_signed:
            return None

        elif not a._is_signed and b._is_signed:
            return None

        else:
            return a

    elif type(a) is IntType and type(b) is AutoIntType:
        return a

    elif type(a) is AutoIntType and type(b) is IntType:
        return b

    elif type(a) is AutoIntType and type(b) is AutoIntType:
        return get_concrete_type(a)

    else:
        raise Todo()

def get_concrete_type(t):
    if type(t) is AutoIntType:
        return IntType()
    else:
        return t
