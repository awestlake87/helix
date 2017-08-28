
from ..err import Todo
from ..dep import GlobalTarget

from .scope import Scope

class GlobalSymbol:
    def __init__(self, unit, ast, parent_scope):
        super().__init__()

        self.unit = unit
        self.ast = ast
        self.parent_scope = parent_scope

        if self.ast.is_cglobal:
            self.scoped_id = None
        else:
            self.scoped_id = [ unit.id, self.ast.id ]

        self._target = None
        self._ir_value = None

        self.init_expr = None

    def _on_ir(self, value):
        self._ir_value = value

    def get_target(self):
        if self._target is None:
            self._target = GlobalTarget(
                self, self._on_ir
            )

        return self._target

    def get_ir_value(self):
        if self._ir_value is None:
            raise Todo()

        else:
            return self._ir_value
