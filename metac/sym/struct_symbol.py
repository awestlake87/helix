
from ..err import Todo
from ..dep import StructTarget

class StructSymbol:
    def __init__(self, unit, parent_scope, ast):
        self.unit = unit
        self.parent_scope = parent_scope
        self.ast = ast

        self._target = None
        self._ir_value = None

    def _on_ir(self, value):
        self._ir_value = value

    def get_target(self):
        if self._target is None:
            self._target = StructTarget(self, on_ir=self._on_ir)

        return self._target

    def get_ir_value(self):
        if self._ir_value is None:
            raise Todo()
        else:
            return self._ir_value
