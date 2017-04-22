
from ...ir import PtrType, Type
from ...err import Todo

from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode
from ..values import SymbolNode

class PtrExprNode(UnaryExprNode):
    def gen_unit_value(self, unit):
        value = self._operand.gen_unit_value(unit)

        if value.is_type():
            return PtrType(value)
        else:
            raise Todo("dereferencing values")

class PreIncExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_pre_inc(self._operand.gen_fun_value(fun))

class PostIncExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_post_inc(self._operand.gen_fun_value(fun))

class PreDecExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_pre_dec(self._operand.gen_fun_value(fun))

class PostDecExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_post_dec(self._operand.gen_fun_value(fun))

class NegExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_negate(self._operand.gen_fun_value(fun))

class InitExprNode(BinaryExprNode):
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

class AssignExprNode(BinaryExprNode):
    def gen_unit_value(self, unit):
        raise Todo()

    def gen_fun_value(self, fun):
        return self._lhs.gen_fun_value(fun).assign(
            self._rhs.gen_fun_value(fun)
        )

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
