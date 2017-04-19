
from ...ir import PtrType, Type
from ...err import Todo

from ..expr_node import ExprNode
from ..values import SymbolNode

class PtrExprNode(ExprNode):
    def __init__(self, expr):
        self._expr = expr

    def gen_unit_value(self, unit):
        value = self._expr.gen_unit_value(unit)

        if value.is_type():
            return PtrType(value)
        else:
            raise Todo("dereferencing values")

class InitExprNode(ExprNode):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def gen_unit_value(self, unit):
        raise Todo()

    def gen_fun_value(self, fun):
        if type(self._lhs) is SymbolNode:
            value = self._rhs.gen_fun_value(fun)
            return fun.symbols.insert(
                self._lhs._id,
                fun.create_stack_var(value.type).initialize(value)
            )
        else:
            raise Todo()

class CallExprNode(ExprNode):
    def __init__(self, lhs, args):
        self._lhs = lhs
        self._args = args

    def gen_unit_value(self, unit):
        return self._lhs.gen_unit_value(unit).call(
            unit, [ arg.gen_unit_value(unit) for arg in self._args ]
        )

    def gen_fun_value(self, fun):
        return self._lhs.gen_fun_value(fun).call(
            fun, [ arg.gen_fun_value(fun) for arg in self._args ]
        )
