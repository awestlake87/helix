
from ...ir import Fun
from ...err import Todo

from ..expr_node import ExprNode

from ...dep import (
    MetaFunSymbol, MetaOverloadSymbol, ExternFunSymbol, InternFunSymbol
)

class FunNode(ExprNode):
    EXTERN_C = 0
    INTERN_C = 1
    META     = 2

    def __init__(self, type, id, param_ids, linkage, body):
        self._type = type
        self._id = id
        self._param_ids = param_ids
        self._linkage = linkage
        self._body = body

        self._symbol = None

    def hoist(self, scope):
        if self._linkage == FunNode.META:
            self._symbol = MetaOverloadSymbol(
                scope,
                self._id,
                self._type,
                self._param_ids,
                self._body
            )

            if scope.has_local(self._id):
                symbol = scope.resolve(self._id)

                if symbol.can_overload():
                    symbol.add_overload(self._symbol)
                else:
                    raise Todo()

            else:
                scope.insert(
                    self._id, MetaFunSymbol(self._id, [ self._symbol ])
                )

        elif self._linkage == FunNode.EXTERN_C:
            self._symbol = ExternFunSymbol(
                scope,
                self._id,
                self._type,
                self._param_ids,
                self._body
            )
            scope.insert(self._id, self._symbol)

        elif self._linkage == FunNode.INTERN_C:
            self._symbol = InternFunSymbol(
                scope,
                self._id,
                self._type,
                self._param_ids,
                self._body
            )
            scope.insert(self._id, self._symbol)

        else:
            raise Todo()

    def get_deps(self, scope):
        if (
            self._linkage == FunNode.EXTERN_C or
            self._linkage == FunNode.INTERN_C
        ):
            return [ self._symbol.get_target() ]
        else:
            return [ ]

    def _create_ir_fun(self, unit):
        linkage = None

        if self._linkage == FunNode.EXTERN_C:
            linkage = Fun.EXTERN_C
        elif self._linkage == FunNode.INTERN_C:
            linkage = Fun.INTERN_C
        else:
            raise Todo("handle error")

        return Fun(
            unit,
            self._type.gen_unit_value(unit),
            self._id,
            self._param_ids,
            linkage
        )

    def hoist_unit_code(self, unit):
        self._fun = self._create_ir_fun(unit)

        unit.symbols.insert(self._id, self._fun)

    def gen_unit_value(self, unit):
        self._fun.create_body()

        self._body.hoist_fun_code(self._fun)
        self._body.gen_fun_code(self._fun)

        return self._fun


    def hoist_fun_code(self, fun):
        self._fun = self._create_ir_fun(fun.unit)

        fun.symbols.insert(self._id, self._fun)

    def gen_fun_value(self, fun):
        return self.gen_unit_value(fun.unit)
