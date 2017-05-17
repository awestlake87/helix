
from ...err import Todo

from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode

from ...ir import (
    gen_fun_assign,

    gen_fun_neg,

    gen_fun_add,
    gen_fun_sub,
    gen_fun_mul,
    gen_fun_div,
    gen_fun_mod,

    gen_fun_pre_inc,
    gen_fun_pre_dec,
    gen_fun_post_inc,
    gen_fun_post_dec,
)

class AddExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_add(
            fun, self._lhs.gen_fun_value(fun), self._rhs.gen_fun_value(fun)
        )

class SubExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_sub(
            fun, self._lhs.gen_fun_value(fun), self._rhs.gen_fun_value(fun)
        )

class MulExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_mul(
            fun, self._lhs.gen_fun_value(fun), self._rhs.gen_fun_value(fun)
        )

class DivExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_div(
            fun, self._lhs.gen_fun_value(fun), self._rhs.gen_fun_value(fun)
        )

class ModExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_mod(
            fun, self._lhs.gen_fun_value(fun), self._rhs.gen_fun_value(fun)
        )



class AddAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return gen_fun_assign(
            fun,
            lhs,
            gen_fun_add(fun, lhs, self._rhs.gen_fun_value(fun))
        )

class SubAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return gen_fun_assign(
            fun,
            lhs,
            gen_fun_sub(fun, lhs, self._rhs.gen_fun_value(fun))
        )

class MulAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return gen_fun_assign(
            fun,
            lhs,
            gen_fun_mul(fun, lhs, self._rhs.gen_fun_value(fun))
        )

class DivAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return gen_fun_assign(
            fun,
            lhs,
            gen_fun_div(fun, lhs, self._rhs.gen_fun_value(fun))
        )

class ModAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return gen_fun_assign(
            fun,
            lhs,
            gen_fun_mod(fun, lhs, self._rhs.gen_fun_value(fun))
        )



class PreIncExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_pre_inc(fun, self._operand.gen_fun_value(fun))

class PostIncExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_post_inc(fun, self._operand.gen_fun_value(fun))

class PreDecExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_pre_dec(fun, self._operand.gen_fun_value(fun))

class PostDecExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_post_dec(fun, self._operand.gen_fun_value(fun))



class NegExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_neg(fun, self._operand.gen_fun_value(fun))
