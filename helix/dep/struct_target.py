
from .target import Target

from .gen_deps import gen_expr_deps

from ..ir import StructType, gen_static_expr_ir

class StructTarget(Target):
    def __init__(self, symbol, on_ir=lambda val: None):
        super().__init__([ ])

        from ..sym import (
            DataAttrSymbol,
            AttrFunSymbol,
            ConstructOperSymbol,
            DestructOperSymbol
        )

        self.symbol = symbol
        self.attrs = { }

        self._on_ir = on_ir

    def build(self):
        from ..sym import DataAttrSymbol

        data = [ ]

        for attr_id, symbol in self.symbol.attrs:
            if type(symbol) is DataAttrSymbol:
                data.append(symbol)
                symbol.set_ir_type(
                    gen_static_expr_ir(
                        self.symbol.parent_scope, symbol.ast.type
                    )
                )

        self._on_ir(
            StructType(
                self.attrs,
                [
                    (
                        member.get_ir_type(),
                        member.id
                    )
                    for member in
                    data
                ]
            )
        )
