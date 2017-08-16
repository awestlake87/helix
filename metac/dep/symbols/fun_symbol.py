
from ..scope import Scope
from ..target import Target

from ..get_deps import get_expr_deps, get_block_deps

from ...ir import FunType, FunValue, gen_static_expr_ir, gen_code

class FunTarget(Target):
    def __init__(self, symbol, on_ir=lambda val: None):
        self.symbol = symbol

        self._on_ir = on_ir

        deps = [ ]

        with self.symbol.unit.use_scope(self.symbol.parent_scope):
            deps += get_expr_deps(self.symbol.unit, self.symbol.ast.type)

        with self.symbol.unit.use_scope(self.symbol.scope):
            deps += get_block_deps(self.symbol.unit, self.symbol.ast.body)

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
