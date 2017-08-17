
from .target import Target

from .gen_deps import gen_expr_deps

from ..ir import StructType, gen_static_expr_ir

class StructTarget(Target):
    def __init__(self, symbol, on_ir=lambda val: None):
        self.symbol = symbol

        self._on_ir = on_ir

        deps = [ ]
        for attr_type, _ in self.symbol.ast.attrs:
            with self.symbol.unit.use_scope(self.symbol.parent_scope):
                deps += gen_expr_deps(self.symbol.unit, attr_type)

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
