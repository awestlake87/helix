
from llvmlite import ir

from .types import AutoIntType, AutoPtrType


class LlvmValue:
    def __init__(self, ir_type, llvm_value):
        self.type = ir_type
        self._llvm_value = llvm_value

    def get_llvm_value(self):
        assert self._llvm_value is not None
        return self._llvm_value

class LlvmRef:
    def __init__(self, ctx, ir_type, llvm_ptr):
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
        self.ctx = ctx

        with self.ctx.builder.goto_block(self.ctx.entry):
            super().__init__(
                ctx, ir_type, self.ctx.builder.alloca(ir_type.get_llvm_value())
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
