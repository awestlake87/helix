from .target import Target

from .gen_deps import gen_expr_deps, gen_block_deps

from ..err import Todo
from ..ast import BangNode, VoidTypeNode
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

    def build(self):
        from ..sym import mangle_name

        ret_node = self.symbol.ast.type.ret_type
        ret_type = type(ret_node)
        ret_ir_type = None

        if ret_type is BangNode:
            ret_ir_type = gen_static_expr_ir(
                self.symbol.parent_scope,
                self.symbol.ast.type.ret_type.operand
            )
        elif ret_type is VoidTypeNode:
            ret_ir_type = gen_static_expr_ir(
                self.symbol.parent_scope, ret_node
            )

        else:
            raise Todo(ret_type)

        param_types = [ ]

        for t in self.symbol.ast.type.param_types:
            if type(t) is BangNode:
                param_types.append(
                    gen_static_expr_ir(self.symbol.parent_scope, t.operand)
                )

        fun_type = FunType(
            ret_ir_type,
            param_types,
            self.is_vargs
        )

        id = ""

        if self.symbol.ast.is_cfun:
            id = self.symbol.ast.id

        else:
            id = mangle_name(self.symbol.scoped_id)

        self.ir_value = FunValue(
            self.symbol.unit, id, fun_type
        )

        if self.symbol.ast.body is not None:
            self.symbol.unit.target.deps.append(FunTarget(self))

        self._on_ir(self.ir_value)


class AttrFunProtoTarget(Target):
    def __init__(self, symbol, on_ir=lambda val: None):
        self.symbol = symbol
        self._on_ir = on_ir

        self.ir_value = None

        with self.symbol.unit.use_scope(self.symbol.parent_scope):
            super().__init__(
                [ self.symbol.struct.target ] +
                gen_expr_deps(self.symbol.unit, self.symbol.ast.type)
            )

    def build(self):
        from ..sym import mangle_name

        ret_node = self.symbol.ast.type.ret_type
        ret_type = type(ret_node)
        ret_ir_type = None

        if ret_type is BangNode:
            ret_ir_type = gen_static_expr_ir(
                self.symbol.parent_scope,
                self.symbol.ast.type.ret_type.operand
            )
        elif ret_type is VoidTypeNode:
            ret_ir_type = gen_static_expr_ir(self.symbol.parent_scope, ret_node)

        else:
            raise Todo(ret_type)

        param_types = [ PtrType(self.symbol.struct.get_ir_value()) ]

        for t in self.symbol.ast.type.param_types:
            if type(t) is BangNode:
                param_types.append(
                    gen_static_expr_ir(self.symbol.parent_scope, t.operand)
                )

        fun_type = FunType(
            ret_ir_type,
            param_types
        )


        id = ""

        if self.symbol.ast.is_cfun:
            id = self.symbol.ast.id

        else:
            id = mangle_name(self.symbol.scoped_id)

        self.ir_value = FunValue(
            self.symbol.unit, id, fun_type
        )

        if self.symbol.ast.body is not None:
            self.symbol.unit.target.deps.append(FunTarget(self))

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

    def build(self):
        gen_code(
            self.proto_target.ir_value,
            self.proto_target.symbol.scope,
            self.proto_target.symbol.ast
        )
