
from ..err import Todo
from ..ir import StructType, gen_static_expr_ir

from .target import Target

class StructTarget(Target):
    def __init__(self, symbol):
        super().__init__([ ])

        self.symbol = symbol
        self.attrs = { }

        self._ir_value = None

    @property
    def ir_value(self):
        if self._ir_value is not None:
            return self._ir_value

        else:
            raise Todo("struct has not been built yet")

    def build(self):
        from ..sym import DataAttrSym

        data = [ ]

        for attr_id, symbol in self.symbol.attrs:
            if type(symbol) is DataAttrSym:
                data.append(symbol)
                symbol.ir_type = gen_static_expr_ir(
                    self.symbol.parent_scope, symbol.ast.type
                )

        self._ir_value = StructType(
            self.attrs,
            [
                (
                    member.ir_type,
                    member.id
                )
                for member in
                data
            ]
        )
