
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

    def __eq__(self, rhs):
        if type(rhs) is PtrType and self.pointee == rhs.pointee:
            return True

        else:
            return False

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

class ArrayType(Type):
    def __init__(self, length, elem_type):
        if type(length) is IntValue and issubclass(type(elem_type), Type):
            self.length = length
            self.elem_type = elem_type

            self._llvm_value = ir.ArrayType(
                self.elem_type.get_llvm_value(),
                self.length.value
            )

        else:
            raise Todo(elem_type)

    def get_llvm_value(self):
        return self._llvm_value


class IrValue:
    pass

class LlvmValue(IrValue):
    def __init__(self, ir_type, llvm_value):
        self.type = ir_type
        self._llvm_value = llvm_value

    def get_llvm_value(self):
        assert self._llvm_value is not None
        return self._llvm_value

class LlvmRef(IrValue):
    def __init__(self, ctx, ir_type, llvm_ptr):
        self.ctx = ctx
        self.type = ir_type
        self._llvm_ptr = llvm_ptr

    def get_llvm_ptr(self):
        assert self._llvm_ptr is not None
        return self._llvm_ptr

    def get_llvm_value(self):
        return self.ctx.builder.load(self.get_llvm_ptr())

class UnitValue(LlvmValue):
    def __init__(self, id):
        self.id = id

        super().__init__(None, ir.Module(id))

class FunValue(LlvmValue):
    def __init__(self, unit, id, ir_type):
        self.unit = unit
        self.id = id

        super().__init__(
            ir_type,
            ir.Function(
                unit.get_ir_value().get_llvm_value(),
                ir_type.get_llvm_value(),
                self.id
            )
        )

class StackValue(LlvmRef):
    def __init__(self, ctx, ir_type):
        with ctx.builder.goto_block(ctx.entry):
            super().__init__(
                ctx, ir_type, ctx.builder.alloca(ir_type.get_llvm_value())
            )

class IntValue(LlvmValue):
    def __init__(self, ir_type, value):
        self.value = value

        if type(ir_type) is AutoIntType:
            super().__init__(ir_type, None)

        else:
            super().__init__(ir_type, ir_type.get_llvm_value()(self.value))

class NilValue(LlvmValue):
    def __init__(self, ir_type):
        if type(ir_type) is AutoPtrType:
            super().__init__(ir_type, None)

        else:
            super().__init__(
                ir_type, ir.IntType(32)(0).inttoptr(ir_type.get_llvm_value())
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
