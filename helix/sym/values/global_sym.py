from ...err import Todo

from ..scope import Scope
from ..manglers import mangle_name

class GlobalSym:
    def __init__(self, unit, ast, parent_scope):
        from ...targets import GlobalTarget
        
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
