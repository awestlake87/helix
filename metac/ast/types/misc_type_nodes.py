
from ..expr_node import ExprNode

from ...err import Todo
from ...ir import FunType, IntType

from ...dep import IntTypeSymbol

class FunTypeNode(ExprNode):
    def __init__(self, ret_type, param_types):
        self._ret_type = ret_type
        self._param_types = param_types

    def hoist(self, scope):
        self._ret_type.hoist(scope)

        for param_type in self._param_types:
            param_type.hoist(scope)

    def get_deps(self, scope):
        deps = [ ]

        deps += self._ret_type.get_deps(scope)

        for param_type in self._param_types:
            target = param_type.get_value(scope).get_target()
            if target:
                deps.append(target)

        return deps

    def gen_unit_value(self, unit):
        return FunType(
            self._ret_type.gen_unit_value(unit),
            [ t.gen_unit_value(unit) for t in self._param_types ]
        )

    def gen_fun_value(self, fun):
        return self.gen_unit_value(fun.unit)

class IntTypeNode(ExprNode):
    def __init__(self, num_bits, is_signed):
        self._num_bits = num_bits
        self._is_signed = is_signed

        self._symbol = IntTypeSymbol()

    def get_value(self, scope):
        return self._symbol

    def gen_unit_value(self, unit):
        return IntType(self._num_bits, self._is_signed)

    def gen_fun_value(self, fun):
        return self.gen_unit_value(fun.unit)
