
from ..err import Todo
from ..dep import FunProtoTarget, AttrFunProtoTarget

from .scope import Scope

class FunSymbol:
    def __init__(self, unit, ast, parent_scope):
        super().__init__()

        self.unit = unit
        self.ast = ast
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)
        self.is_vargs = ast.is_vargs

        self._target = None
        self._ir_prototype = None

    def _on_ir(self, value):
        self._ir_prototype = value

    def get_target(self):
        if self._target is None:
            self._target = FunProtoTarget(
                self, self._on_ir, is_vargs=self.is_vargs
            )

        return self._target

    def get_ir_value(self):
        if self._ir_prototype is None:
            raise Todo()

        else:
            return self._ir_prototype

class AttrFunSymbol:
    def __init__(self, unit, struct, ast, parent_scope):
        super().__init__()

        self.unit = unit
        self.struct = struct
        self.ast = ast
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)

        self._target = None
        self._ir_prototype = None

    def _on_ir(self, value):
        self._ir_prototype = value

    def get_target(self):
        if self._target is None:
            self._target = AttrFunProtoTarget(self, self._on_ir)

        return self._target

    def get_ir_value(self):
        if self._ir_prototype is None:
            raise Todo()

        else:
            return self._ir_prototype
