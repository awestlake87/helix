
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

        self.target = GlobalTarget(self)
        self._ir_value = None

        self.type = None
        self.init_expr = None

    @property
    def ir_value(self):
        return self.target.ir_value
