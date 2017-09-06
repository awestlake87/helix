
from ..err import Todo
from ..ast import BangNode, VoidTypeNode
from ..ir import FunType, FunValue, PtrType, gen_static_expr_ir, gen_code

from .scope import Scope
from .target import Target

class FunProtoTarget(Target):
    def __init__(self, symbol, is_vargs=False):
        super().__init__([ ])

        self.symbol = symbol
        self.is_vargs = is_vargs

        self._ir_value = None

    @property
    def ir_value(self):
        if self._ir_value is not None:
            return self._ir_value

        else:
            raise Todo("fun proto has not been built")

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

        self._ir_value = FunValue(
            self.symbol.unit, id, fun_type
        )


class AttrFunProtoTarget(Target):
    def __init__(self, symbol):
        super().__init__([ symbol.struct.target ])

        self.symbol = symbol

        self._ir_value = None

    @property
    def ir_value(self):
        if self._ir_value is not None:
            return self._ir_value

        else:
            raise Todo("attr fun proto has not been built")

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

        param_types = [ PtrType(self.symbol.struct.ir_value) ]

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

        self._ir_value = FunValue(
            self.symbol.unit, id, fun_type
        )


class FunTarget(Target):
    def __init__(self, proto_target):
        super().__init__([ proto_target ])
        self.proto_target = proto_target

        symbol = self.proto_target.symbol

    def build(self):
        gen_code(
            self.proto_target.ir_value,
            self.proto_target.symbol.scope,
            self.proto_target.symbol.ast
        )

class FunSymbol:
    def __init__(self, unit, ast, parent_scope):
        self.unit = unit
        self.ast = ast
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)
        self.is_vargs = ast.is_vargs

        if self.ast.is_cfun:
            self.scoped_id = None
        else:
            self.scoped_id = [ unit.id, self.ast.id ]

        self.proto_target = FunProtoTarget(
            self, is_vargs=self.is_vargs
        )

        if self.ast.body is not None:
            self.target = FunTarget(self.proto_target)

        else:
            self.target = None
    @property
    def ir_value(self):
        return self.proto_target.ir_value

class AttrFunSymbol:
    def __init__(self, unit, struct, ast, parent_scope):
        self.unit = unit
        self.struct = struct
        self.ast = ast
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)

        if self.ast.is_cfun:
            self.scoped_id = None
        else:
            self.scoped_id = [ unit.id, struct.id, self.ast.id ]

        self.proto_target = AttrFunProtoTarget(self)
        self.target = FunTarget(self.proto_target)

    @property
    def ir_value(self):
        return self.proto_target.ir_value
