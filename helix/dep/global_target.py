from .target import Target

from .gen_deps import gen_expr_deps
from ..ir import (
    gen_static_expr_ir,
    gen_static_as_ir,
    GlobalValue,
    AutoType,
    get_concrete_type
)

class GlobalTarget(Target):
    def __init__(self, symbol, on_ir=lambda val: None, is_vargs=False):
        super().__init__([ ])

        self.symbol = symbol
        self._on_ir = on_ir

        self.ir_value = None

    def build(self):
        from ..sym import mangle_name

        id = ""

        if self.symbol.ast.is_cglobal:
            id = self.symbol.ast.id

        else:
            id = mangle_name(self.symbol.scoped_id)

        with self.symbol.unit.use_scope(self.symbol.parent_scope):
            ir_type = gen_static_expr_ir(
                self.symbol.parent_scope, self.symbol.ast.type
            )

            deduce_type = type(ir_type) is AutoType

            ir_initializer = None

            if self.symbol.init_expr is not None:
                ir_initializer = gen_static_expr_ir(
                    self.symbol.parent_scope, self.symbol.init_expr
                )

                if deduce_type:
                    ir_type = get_concrete_type(ir_initializer.type)

                ir_initializer = gen_static_as_ir(
                    self.symbol.parent_scope, ir_initializer, ir_type
                )

            elif deduce_type:
                raise Todo()


            self.ir_value = GlobalValue(
                self.symbol.unit, id, ir_type, ir_initializer
            )

        self._on_ir(self.ir_value)
