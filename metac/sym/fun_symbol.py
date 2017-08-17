
from ..err import Todo
from ..dep import FunTarget

from .scope import Scope

class FunSymbol:
    def __init__(self, unit, ast, parent_scope):
        super().__init__()

        self.unit = unit
        self.ast = ast
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)

        self._target = None
        self._ir_value = None

    def _on_ir(self, value):
        self._ir_value = value

    def get_target(self):
        if self._target is None:
            self._target = FunTarget(self, self._on_ir)

        return self._target

    def get_ir_value(self):
        if self._ir_value is None:
            raise Todo()

        else:
            return self._ir_value
