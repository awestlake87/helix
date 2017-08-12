from contextlib import contextmanager

from ...err import ReturnTypeMismatch, NotApplicable, Todo
from ..symbols import SymbolTable
from .values import *
from ..types import *

from llvmlite import ir

class Fun(Value):
    def __init__(self, unit, type, id, param_ids):
        self.unit = unit
        self.type = type

        self._builder = None
        self._id = id
        self._fun = ir.Function(
            unit._module, self.type.get_llvm_type(), id
        )
        self._fun.linkage = "external"

        for arg, id in zip(self._fun.args, param_ids):
            arg.name = id

    def create_body(self):
        self._entry = self._fun.append_basic_block("entry")

        self._builder = ir.IRBuilder(self._entry)

        self._body = self._builder.append_basic_block("body")
        self._builder.branch(self._body)
        self._builder.position_at_end(self._body)

        self.symbols = SymbolTable(self.unit.symbols)

        for type, arg in zip(self.type._param_types, self._fun.args):
            self.symbols.insert(arg.name, ConstLlvmValue(type, arg))

    def create_stack_var(self, ir_type):
        llvm_value = None

        if type(ir_type) is AutoIntType:
            with self._builder.goto_block(self._entry):
                var_type = IntType()
                llvm_value = self._builder.alloca(
                    var_type.get_llvm_type()
                )

                return FunLlvmLVal(self, var_type, llvm_value)

        else:
            with self._builder.goto_block(self._entry):
                llvm_value = self._builder.alloca(
                    ir_type.get_llvm_type()
                )

                return FunLlvmLVal(self, ir_type, llvm_value)

    @contextmanager
    def using_scope(self, symbols):
        old_symbols = self.symbols
        self.symbols = symbols

        yield

        self.symbols = old_symbols

    def is_rval(self):
        return True

    def get_llvm_rval(self):
        return self._fun
