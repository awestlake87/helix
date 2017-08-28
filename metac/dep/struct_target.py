
from .target import Target

from .gen_deps import gen_expr_deps

from ..ir import StructType, gen_static_expr_ir

class StructTarget(Target):
    def __init__(self, symbol, on_ir=lambda val: None):
        from ..sym import DataAttrSymbol, AttrFunSymbol

        self.symbol = symbol
        self.attrs = { }

        self._on_ir = on_ir

        deps = [ ]

        for attr_id, attr_symbol in self.symbol.attrs:
            with self.symbol.unit.use_scope(self.symbol.parent_scope):
                attr_type = type(attr_symbol)

                if attr_type is DataAttrSymbol:
                    deps += gen_expr_deps(
                        self.symbol.unit, attr_symbol.ast.type
                    )
                    self.attrs[attr_id] = attr_symbol

                elif attr_type is AttrFunSymbol:
                    self.attrs[attr_id] = attr_symbol

        super().__init__(deps)

    def _build_target(self):
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
