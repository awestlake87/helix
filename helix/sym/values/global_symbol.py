from ...err import Todo
from ...ir import (
    gen_static_expr_ir,
    gen_static_as_ir,
    GlobalValue,
    AutoType,
    get_concrete_type
)

from ..scope import Scope
from ..target import Target
from ..manglers import mangle_name

class GlobalTarget(Target):
    def __init__(self, symbol):
        super().__init__([ ])

        self.symbol = symbol

        self._ir_value = None

    @property
    def ir_value(self):
        if self._ir_value is not None:
            return self._ir_value

        else:
            raise Todo("global has not been built yet")

    def build(self):
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

            self._ir_value = GlobalValue(
                self.symbol.unit, id, ir_type, ir_initializer
            )


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
