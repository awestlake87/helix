
from ..err import Todo
from ..sym import BangSym, VoidTypeSym
from ..ir import FunType, FunValue, PtrType, gen_static_expr_ir, gen_code
from ..check import check_ownership

from .target import Target

class FunProtoTarget(Target):
    def __init__(
        self, unit, parent_scope, type_node, absolute_id, is_vargs=False
    ):
        super().__init__([ ])

        self.unit = unit
        self.parent_scope = parent_scope
        self.type_node = type_node
        self.absolute_id = absolute_id
        self.is_vargs = is_vargs

        self._ir_value = None

    @property
    def ir_value(self):
        if self._ir_value is not None:
            return self._ir_value

        else:
            raise Todo("fun proto has not been built")

    def build(self):
        ret_node = self.type_node.ret_type
        ret_type = type(ret_node)
        ret_ir_type = None

        if ret_type is BangSym:
            ret_ir_type = gen_static_expr_ir(
                self.parent_scope,
                self.type_node.ret_type.operand
            )
        elif ret_type is VoidTypeSym:
            ret_ir_type = gen_static_expr_ir(
                self.parent_scope, ret_node
            )

        else:
            raise Todo(ret_type)

        param_types = [ ]

        for t in self.type_node.param_types:
            if type(t) is BangNode:
                param_types.append(
                    gen_static_expr_ir(self.parent_scope, t.operand)
                )

        fun_type = FunType(
            ret_ir_type,
            param_types,
            self.is_vargs
        )

        self._ir_value = FunValue(self.unit, self.absolute_id, fun_type)


class AttrFunProtoTarget(Target):
    def __init__(self, unit, struct, parent_scope, type_node, absolute_id):
        super().__init__([ struct.target ])

        self.unit = unit
        self.struct = struct
        self.parent_scope = parent_scope
        self.type_node = type_node
        self.absolute_id = absolute_id

        self._ir_value = None

    @property
    def ir_value(self):
        if self._ir_value is not None:
            return self._ir_value

        else:
            raise Todo("attr fun proto has not been built")

    def build(self):
        ret_node = self.type_node.ret_type
        ret_type = type(ret_node)
        ret_ir_type = None

        if ret_type is BangNode:
            ret_ir_type = gen_static_expr_ir(
                self.parent_scope,
                self.type_node.ret_type.operand
            )
        elif ret_type is VoidTypeNode:
            ret_ir_type = gen_static_expr_ir(self.parent_scope, ret_node)

        else:
            raise Todo(ret_type)

        param_types = [ PtrType(self.struct.ir_value) ]

        for t in self.type_node.param_types:
            if type(t) is BangNode:
                param_types.append(
                    gen_static_expr_ir(self.parent_scope, t.operand)
                )

        fun_type = FunType(
            ret_ir_type,
            param_types
        )

        self._ir_value = FunValue(self.unit, self.absolute_id, fun_type)

class FunTarget(Target):
    def __init__(self, proto_target, scope, fun_sym):
        super().__init__([ proto_target ])

        self.proto_target = proto_target
        self.scope = scope
        self.fun_sym = fun_sym

    def build(self):
        check_ownership(self.fun_sym.body)
        gen_code(
            self.proto_target.ir_value,
            self.scope,
            self.fun_sym
        )
