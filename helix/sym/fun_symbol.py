
from ..err import Todo
from ..dep import FunProtoTarget, AttrFunProtoTarget, FunTarget

from .scope import Scope

class FunSymbol:
    def __init__(self, unit, ast, parent_scope):
        self.unit = unit
        self.ast = ast
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)
        self.is_vargs = ast.is_vargs

        if self.ast.is_cfun:
            self.scoped_id = None
        else:
            self.scoped_id = [ unit.id, self.ast.id ]

        self.proto_target = FunProtoTarget(
            self, self._on_ir, is_vargs=self.is_vargs
        )

        if self.ast.body is not None:
            self.target = FunTarget(self.proto_target)

        else:
            self.target = None

        self._ir_prototype = None

    def _on_ir(self, value):
        self._ir_prototype = value

    def get_ir_value(self):
        if self._ir_prototype is None:
            raise Todo()

        else:
            return self._ir_prototype

class AttrFunSymbol:
    def __init__(self, unit, struct, ast, parent_scope):
        self.unit = unit
        self.struct = struct
        self.ast = ast
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)

        if self.ast.is_cfun:
            self.scoped_id = None
        else:
            self.scoped_id = [ unit.id, struct.id, self.ast.id ]

        self.proto_target = AttrFunProtoTarget(self, self._on_ir)
        self.target = FunTarget(self.proto_target)

        self._ir_prototype = None

    def _on_ir(self, value):
        self._ir_prototype = value

    def get_ir_value(self):
        if self._ir_prototype is None:
            raise Todo()

        else:
            return self._ir_prototype
