
from .expr_node import BinaryExprNode, UnaryExprNode

from ..err import Todo

class AndNode(BinaryExprNode):
    def gen_unit_code(self, unit):
        raise Todo()

    def gen_fun_code(self, fun):
        raise Todo()

class OrNode(BinaryExprNode):
    def gen_unit_code(self, unit):
        raise Todo()

    def gen_fun_code(self, fun):
        raise Todo()

class NotNode(UnaryExprNode):
    def gen_unit_code(self, unit):
        raise Todo()

    def gen_fun_code(self, fun):
        raise Todo()


class LtnExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_ltn(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class GtnExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_gtn(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class LeqExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_leq(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class GeqExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_geq(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )


class EqNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_eq(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )
class NeqNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_neq(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )
