from contextlib import contextmanager
from llvmlite import binding

from ...err import Todo
from ...ir import UnitValue
from ...ast import *

from ..target import Target
from ..scope import Scope

class UnitTarget(Target):
    def __init__(self, symbol, on_llvm_module=lambda m: None):
        super().__init__([ ])

        self.symbol = symbol
        self._on_llvm_module = on_llvm_module

    def build(self):
        try:
            llvm_module = binding.parse_assembly(
                str(self.symbol.ir_value.get_llvm_value())
            )

            llvm_module.verify()

            self._on_llvm_module(llvm_module)

        except Exception as e:
            print(e)
            print(self.symbol.ir_value.get_llvm_value())

            raise e

class UnitSym:
    def __init__(self, id, ast):
        self.ast = ast
        self.scope = Scope()

        self.id = id
        self.ir_value = UnitValue(self.id)

        self.target = UnitTarget(
            self, on_llvm_module=self._on_llvm_module
        )

        self._llvm_module = None

    def _on_llvm_module(self, module):
        self._llvm_module = module

    def get_llvm_module(self):
        return self._llvm_module

    def get_ir_value(self):
        return self.ir_value

    @contextmanager
    def use_scope(self, scope):
        assert not scope is None

        old_scope = self.scope
        self.scope = scope

        yield

        self.scope = old_scope
