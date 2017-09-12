
from ...err import Todo
from ...sym import BangSym, VoidTypeSym

from ..scope import Scope
from ..manglers import mangle_name

class FunSym:
    def __init__(
        self,
        unit,
        parent_scope,
        type_sym,
        id,
        param_ids,
        body,
        is_vargs = False,
        is_cfun = False,
        is_attr = False
    ):
        from ...targets import FunProtoTarget, FunTarget

        self.unit = unit
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)

        self.type = type_sym
        self.id = id
        self.param_ids = param_ids
        self.body = body

        self.is_vargs = is_vargs
        self.is_cfun = is_cfun
        self.is_attr = is_attr

        if self.is_cfun:
            self.absolute_id = self.id
        else:
            self.absolute_id = mangle_name([ unit.id, self.id ])

        self.proto_target = FunProtoTarget(
            self.unit,
            self.parent_scope,
            self.type,
            self.absolute_id,
            is_vargs = self.is_vargs
        )

        if self.body is not None:
            self.target = FunTarget(
                self.proto_target, self.scope, self
            )

        else:
            self.target = None

    @property
    def ir_value(self):
        return self.proto_target.ir_value

class AttrFunSym:
    def __init__(self, unit, struct, id, ast, parent_scope):
        from ...targets import AttrFunProtoTarget, FunTarget

        self.unit = unit
        self.struct = struct
        self.id = id
        self.ast = ast
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)

        if self.ast.is_cfun:
            self.absolute_id = self.ast.id
        else:
            self.absolute_id = mangle_name([ unit.id, struct.id, self.id ])

        self.proto_target = AttrFunProtoTarget(
            self.unit,
            self.struct,
            self.parent_scope,
            self.ast.type,
            self.absolute_id
        )
        self.target = FunTarget(self.proto_target, self.scope, self.ast)

    @property
    def ir_value(self):
        return self.proto_target.ir_value
