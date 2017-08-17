from .target import Target

from .gen_deps import gen_expr_deps, gen_block_deps

from ..ir import FunType, FunValue, gen_static_expr_ir, gen_code

class FunTarget(Target):
    def __init__(self, symbol, on_ir=lambda val: None):
        self.symbol = symbol

        self._on_ir = on_ir

        deps = [ ]

        with self.symbol.unit.use_scope(self.symbol.parent_scope):
            deps += gen_expr_deps(self.symbol.unit, self.symbol.ast.type)

        with self.symbol.unit.use_scope(self.symbol.scope):
            deps += gen_block_deps(self.symbol.unit, self.symbol.ast.body)

        super().__init__(deps)

    def _build_target(self):
        fun_type = FunType(
            gen_static_expr_ir(
                self.symbol.parent_scope, self.symbol.ast.type.ret_type
            ),
            [
                gen_static_expr_ir(self.symbol.parent_scope, t)
                for t in
                self.symbol.ast.type.param_types
            ]
        )

        fun_value = FunValue(self.symbol.unit, self.symbol.ast.id, fun_type)

        gen_code(fun_value, self.symbol.scope, self.symbol.ast)

        self._on_ir(fun_value)
