
from ..err import Todo

from llvmlite import ir

class Type:
    pass

class PtrType(Type):
    def __init__(self, pointee):
        self.pointee = pointee

        if type(self.pointee) is AutoPtrType:
            self._llvm_value = None

        else:
            self._llvm_value = self.pointee.get_llvm_value().as_pointer()

    def get_llvm_value(self):
        assert self._llvm_value is not None

        return self._llvm_value

class AutoPtrType(Type):
    def __eq__(self, other):
        return type(other) is AutoPtrType

class IntType(Type):
    def __init__(self, num_bits=32, is_signed=True):
        self.num_bits = num_bits
        self.is_signed = is_signed
        self._llvm_value = ir.IntType(self.num_bits)

    def get_llvm_value(self):
        return self._llvm_value

    def __eq__(self, other):
        return (
            type(other) is IntType and
            self.num_bits == other.num_bits and
            self.is_signed == other.is_signed
        )

def BitType():
    return IntType(1, False)

class AutoIntType(Type):
    def __eq__(self, other):
        return type(other) is AutoIntType

class FunType(Type):
    def __init__(self, ret_type, param_types):
        self.ret_type = ret_type
        self.param_types = param_types

        self._llvm_value = ir.FunctionType(
            self.ret_type.get_llvm_value(),
            [ t.get_llvm_value() for t in self.param_types ]
        )

    def get_llvm_value(self):
        return self._llvm_value

class StructType(Type):
    def __init__(self, attrs=[]):
        self.attrs = attrs
        self._llvm_value = ir.LiteralStructType(
            [ t.get_llvm_value() for t, _ in self.attrs ]
        )

    def get_llvm_value(self):
        return self._llvm_value

    def get_attr_info(self, id):
        for i in range(0, len(self.attrs)):
            attr_type, attr_id = self.attrs[i]

            if attr_id == id:
                return (attr_type, i)

        raise Todo(
            "make a \"unable to resolve struct attr '{}'\" error".format(id)
        )


def get_common_type(a, b):
    if a is b or a == b:
        return a

    elif type(a) is IntType and type(b) is AutoIntType:
        return a

    elif type(a) is AutoIntType and type(b) is IntType:
        return b

    elif type(a) is PtrType and type(b) is AutoPtrType:
        return a

    elif type(a) is AutoPtrType and type(b) is PtrType:
        return b

    else:
        raise Todo()

def get_concrete_type(t):
    if type(t) is AutoIntType:
        return IntType()
    else:
        return t
