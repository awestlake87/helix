from .target import Target

from .gen_deps import gen_expr_deps, gen_block_deps

from ..ir import FunType, FunValue, PtrType, gen_static_expr_ir, gen_code

class FunProtoTarget(Target):
    def __init__(self, symbol, on_ir=lambda val: None, is_vargs=False):
        self.symbol = symbol
        self._on_ir = on_ir
        self.is_vargs = is_vargs

        self.ir_value = None

        with self.symbol.unit.use_scope(self.symbol.parent_scope):
            super().__init__(
                gen_expr_deps(self.symbol.unit, self.symbol.ast.type)
            )

    def _build_target(self):
        from ..sym import mangle_name

        fun_type = FunType(
            gen_static_expr_ir(
                self.symbol.parent_scope, self.symbol.ast.type.ret_type
            ),
            [
                gen_static_expr_ir(self.symbol.parent_scope, t)
                for t in
                self.symbol.ast.type.param_types
            ],
            self.is_vargs
        )

        id = ""

        if self.symbol.ast.is_cfun:
            id = self.symbol.ast.id

        else:
            id = mangle_name(self.symbol.scoped_id)

        print(id)

        self.ir_value = FunValue(
            self.symbol.unit, id, fun_type
        )

        if self.symbol.ast.body is not None:
            self.symbol.unit.get_target().add_dep(FunTarget(self))

        self._on_ir(self.ir_value)


class AttrFunProtoTarget(Target):
    def __init__(self, symbol, on_ir=lambda val: None):
        self.symbol = symbol
        self._on_ir = on_ir

        self.ir_value = None

        with self.symbol.unit.use_scope(self.symbol.parent_scope):
            super().__init__(
                [ self.symbol.struct.get_target() ] +
                gen_expr_deps(self.symbol.unit, self.symbol.ast.type)
            )

    def _build_target(self):
        from ..sym import mangle_name
        
        fun_type = FunType(
            gen_static_expr_ir(
                self.symbol.parent_scope, self.symbol.ast.type.ret_type
            ),
            [ PtrType(self.symbol.struct.get_ir_value()) ] + [
                gen_static_expr_ir(self.symbol.parent_scope, t)
                for t in
                self.symbol.ast.type.param_types
            ]
        )

        id = ""

        if self.symbol.ast.is_cfun:
            id = self.symbol.ast.id

        else:
            id = mangle_name(self.symbol.scoped_id)

        print(id)

        self.ir_value = FunValue(
            self.symbol.unit, id, fun_type
        )

        if self.symbol.ast.body is not None:
            self.symbol.unit.get_target().add_dep(FunTarget(self))

        self._on_ir(self.ir_value)


class FunTarget(Target):
    def __init__(self, proto_target):
        self.proto_target = proto_target

        symbol = self.proto_target.symbol

        with symbol.unit.use_scope(symbol.scope):
            super().__init__(
                [ self.proto_target ] +
                gen_block_deps(symbol.unit, symbol.ast.body)
            )

    def _build_target(self):
        gen_code(
            self.proto_target.ir_value,
            self.proto_target.symbol.scope,
            self.proto_target.symbol.ast
        )
