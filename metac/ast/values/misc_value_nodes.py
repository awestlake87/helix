
from ...ir import NilValue, AutoIntType, IntType, StaticValue
from ...err import Todo

from ..expr_node import ExprNode

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

    def get_value(self, scope):
        return scope.resolve(self._id)

    def gen_unit_value(self, unit):
        return unit.symbols.resolve(self._id)

    def gen_fun_value(self, fun):
        return fun.symbols.resolve(self._id)
