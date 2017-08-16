
from ..target import Target

from ..get_deps import get_expr_deps

from ...ir import StructType, gen_static_expr_ir

class StructTarget(Target):
    def __init__(self, symbol, on_ir=lambda val: None):
        self.symbol = symbol

        self._on_ir = on_ir

        deps = [ ]
        for attr_type, _ in self.symbol.ast.attrs:
            with self.symbol.unit.use_scope(self.symbol.parent_scope):
                deps += get_expr_deps(self.symbol.unit, attr_type)

        super().__init__(deps)

    def _build_target(self):
        self._on_ir(
            StructType([
                (
                    gen_static_expr_ir(self.symbol.parent_scope, attr_type),
                    attr_id
                )
                for attr_type, attr_id in
                self.symbol.ast.attrs
            ])
        )

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
