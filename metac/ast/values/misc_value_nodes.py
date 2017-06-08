
from ...ir import (
    Unit, Fun, NilValue, AutoIntType, IntType, StaticValue, StructType
)
from ...err import Todo

from ..expr_node import ExprNode

from ...dep import (
    Scope,
    UnitSymbol,
    MetaFunSymbol,
    MetaOverloadSymbol,
    ExternFunSymbol,
    InternFunSymbol,
    StructSymbol
)

class UnitNode(ExprNode):
    def __init__(self, block):
        self._block = block
        self._symbol = UnitSymbol(self._block)

    def get_symbol(self):
        return self._symbol

    def gen_module_value(self, module):
        unit = Unit()

        self._block.hoist_unit_code(unit)
        self._block.gen_unit_code(unit)

        return unit

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

        if self._linkage == FunNode.META:
            self._symbol = MetaOverloadSymbol(
                self._type,
                self._param_ids,
                self._body
            )

        elif self._linkage == FunNode.EXTERN_C:
            self._symbol = ExternFunSymbol(
                self._id,
                self._type,
                self._param_ids,
                self._body
            )

        elif self._linkage == FunNode.INTERN_C:
            self._symbol = InternFunSymbol(
                self._id,
                self._type,
                self._param_ids,
                self._body
            )

        else:
            raise Todo()

    def hoist(self, scope):
        if not self._id is None:
            if self._linkage == FunNode.META:
                if scope.has_local(self._id):
                    symbol = scope.resolve(self._id)

                    if symbol.can_overload():
                        symbol.add_overload(self._symbol)
                    else:
                        raise Todo()

                else:
                    scope.insert(
                        self._id,
                        MetaFunSymbol(self._id, [ self._symbol ])
                    )

            elif (
                self._linkage == FunNode.EXTERN_C or
                self._linkage == FunNode.INTERN_C
            ):
                scope.insert(self._id, self._symbol)

            else:
                raise Todo()

        else:
            raise Todo()

    def create_targets(self, scope):
        if (
            self._linkage == FunNode.EXTERN_C or
            self._linkage == FunNode.INTERN_C
        ):
            return [ self._symbol.get_target(scope) ]
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


class AutoIntNode(ExprNode):
    def __init__(self, value, radix=10):
        self._value = value
        self._radix = radix

    def gen_unit_value(self, unit):
        return StaticValue(
            AutoIntType(),
            (
                int(self._value, self._radix)
                if type(self._value) is str else
                self._value
            )
        )

    def gen_fun_value(self, fun):
        return self.gen_unit_value(fun.unit)

class IntNode(ExprNode):
    def __init__(self, num_bits, is_signed, value, radix=10):
        self._num_bits = num_bits
        self._is_signed = is_signed
        self._value = value
        self._radix = radix

    def gen_unit_value(self, unit):
        return StaticValue(
            IntType(self._num_bits, self._is_signed),
            (
                int(self._value, self._radix)
                if type(self._value) is str else
                self._value
            )
        )

    def gen_fun_value(self, fun):
        return self.gen_unit_value(fun.unit)

class NilNode(ExprNode):
    def gen_unit_value(self, unit):
        return NilValue()

    def gen_fun_value(self, fun):
        return self.gen_unit_value(fun.unit)

class SymbolNode(ExprNode):
    def __init__(self, id):
        self._id = id

    def gen_unit_value(self, unit):
        return unit.symbols.resolve(self._id)

    def gen_fun_value(self, fun):
        return fun.symbols.resolve(self._id)


class StructNode(ExprNode):
    def __init__(self, id, attrs = [ ]):
        self._id = id
        self._attrs = attrs
        self._symbol = StructSymbol(id)

    def hoist(self, scope):
        if not self._id is None:
            scope.insert(self._id, self._symbol)

    def create_targets(self, scope):
        return [ self._symbol.get_target(scope) ]

    def gen_unit_value(self, unit):
        return unit.symbols.insert(
            self._id,
            StructType([
                (type.gen_unit_value(unit), id) for type, id in self._attrs
            ])
        )

    def gen_fun_value(self, fun):
        raise Todo()
