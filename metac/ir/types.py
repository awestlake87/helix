
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

class VoidType(Type):
    def __init__(self):
        self._llvm_value = ir.VoidType()

    def get_llvm_value(self):
        return self._llvm_value

    def __eq__(self, other):
        return type(other) is VoidType

def BitType():
    return IntType(1, False)

class AutoIntType(Type):
    def __eq__(self, other):
        return type(other) is AutoIntType

class FunType(Type):
    def __init__(self, ret_type, param_types, is_vargs=False):
        self.ret_type = ret_type
        self.param_types = param_types
        self.is_vargs = is_vargs

        self._llvm_value = ir.FunctionType(
            self.ret_type.get_llvm_value(),
            [ t.get_llvm_value() for t in self.param_types ],
            is_vargs
        )

    def get_llvm_value(self):
        return self._llvm_value

class StructType(Type):
    def __init__(self, attrs, data):
        self.attrs = attrs
        self.data = data
        self._llvm_value = ir.LiteralStructType(
            [ t.get_llvm_value() for t, _ in self.data ]
        )

    def get_llvm_value(self):
        return self._llvm_value

    def get_attr_symbol(self, id):
        if id in self.attrs:
            return self.attrs[id]

        else:
            raise Todo(
                "make a \"unable to resolve struct attr '{}'\" error".format(
                    id
                )
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

class BoundAttrFunValue(LlvmValue):
    def __init__(self, instance, attr_fun):
        self.instance = instance

        super().__init__(attr_fun.type, attr_fun.get_llvm_value())

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
                ir_type, ir_type.get_llvm_value()(None)
            )
