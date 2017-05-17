
from ...err import Todo

from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode

from ...ir import (
    gen_fun_assign,

    gen_fun_bit_and,
    gen_fun_bit_xor,
    gen_fun_bit_or,
    gen_fun_bit_not,
    gen_fun_bit_shr,
    gen_fun_bit_shl
)

class BitAndExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_bit_and(
            fun,
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class BitXorExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_bit_xor(
            fun,
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class BitOrExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_bit_or(
            fun,
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class BitNotExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_bit_not(fun, self._operand.gen_fun_value(fun))

class BitShrExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_bit_shr(
            fun,
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class BitShlExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return gen_fun_bit_shl(
            fun,
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )


class BitAndAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return gen_fun_assign(
            fun,
            lhs,
            gen_fun_bit_and(fun, lhs, self._rhs.gen_fun_value(fun))
        )

class BitXorAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return gen_fun_assign(
            fun,
            lhs,
            gen_fun_bit_xor(fun, lhs, self._rhs.gen_fun_value(fun))
        )

class BitOrAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return gen_fun_assign(
            fun,
            lhs,
            gen_fun_bit_or(fun, lhs, self._rhs.gen_fun_value(fun))
        )

class BitShrAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return gen_fun_assign(
            fun,
            lhs,
            gen_fun_bit_shr(fun, lhs, self._rhs.gen_fun_value(fun))
        )

class BitShlAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return gen_fun_assign(
            fun,
            lhs,
            gen_fun_bit_shl(fun, lhs, self._rhs.gen_fun_value(fun))
        )
