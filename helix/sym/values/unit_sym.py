from contextlib import contextmanager

from ...err import Todo
from ...ast import *

from ..scope import Scope

class UnitSym:
    def __init__(self, id, ast):
        from ...ir import UnitValue
        from ...targets import UnitTarget

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
