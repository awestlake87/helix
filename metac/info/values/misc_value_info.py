from contextlib import contextmanager

from ...err import Todo
from ...scope import Scope

from ..expr_info import ExprInfo
from ..statements import BlockInfo

class IntInfo:
    pass

class NilInfo:
    pass

class GlobalInfo:
    pass

class AttrInfo:
    pass

class StringInfo:
    pass

class Target:
    def __init__(self):
        self.deps = [ ]

        self.built = False
        self.marked = False

    @contextmanager
    def mark(self):
        self.marked = True
        yield
        self.marked = False

class UnitProtoTarget(Target):
    def __init__(self):
        super().__init__()

        self._ir_value = None

    @property
    def ir_value(self):
        if self._ir_value is not None:
            return self._ir_value

        else:
            raise Todo("unit proto target has not been built")

class UnitTarget(Target):
    def __init__(self, proto_target):
        super().__init__()

        self.proto_target = proto_target
        self.deps.append(self.proto_target)

class UnitInfo(ExprInfo):
    def __init__(self, parent_scope = None):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.block = None

        self.proto_target = UnitProtoTarget()
        self.target = UnitTarget(self.proto_target)


class FunProtoTarget(Target):
    def __init__(self, unit_proto, scope, absolute_id, fun_type_info):
        super().__init__()

        self.unit_proto = unit_proto
        self.scope = scope
        self.absolute_id = absolute_id
        self.type = fun_type_info

        self.deps.append(self.unit_proto)

        self._ir_value = None

    @property
    def ir_value(self):
        if self._ir_value is not None:
            return self._ir_value

        else:
            raise Todo("target has not been built")

class FunTarget(Target):
    def __init__(self, proto_target, scope, fun_info):
        super().__init__()

        self.scope = scope
        self.info = fun_info
        self.proto_target = proto_target
        self.deps.append(self.proto_target)

class FunInfo(ExprInfo):
    def __init__(
        self,
        unit,
        parent_scope,
        id,
        fun_type_info,
        param_ids,
        is_cfun = False,
        is_attr = False
    ):
        self.unit = unit
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)
        self.id = id
        self.type = fun_type_info
        self.param_ids = param_ids
        self.is_cfun = is_cfun
        self.is_attr = is_attr

        self.body = None

        absolute_id = None

        if self.is_cfun:
            absolute_id = self.id

        else:
            raise Todo()

        self.proto_target = FunProtoTarget(
            unit.proto_target, self.scope, absolute_id, self.type
        )
        self.target = FunTarget(self.proto_target, self.scope, self)

class VarInfo(ExprInfo):
    pass

class SymbolInfo(ExprInfo):
    def __init__(self, id):
        self.id = id

class AutoIntInfo(ExprInfo):
    def __init__(self, value, radix):
        self.value = value
        self.radix = radix
