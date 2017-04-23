
from ...err import Todo

from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode


class BitAndExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_bit_and(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class BitXorExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_bit_xor(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class BitOrExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_bit_or(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class BitNotExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_bit_not(self._operand.gen_fun_value(fun))

class BitShrExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_bit_shr(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class BitShlExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_bit_shl(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )


class BitAndAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return lhs.assign(fun.gen_bit_and(lhs, self._rhs.gen_fun_value(fun)))

class BitXorAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return lhs.assign(fun.gen_bit_xor(lhs, self._rhs.gen_fun_value(fun)))

class BitOrAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return lhs.assign(fun.gen_bit_or(lhs, self._rhs.gen_fun_value(fun)))

class BitShrAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return lhs.assign(fun.gen_bit_shr(lhs, self._rhs.gen_fun_value(fun)))

class BitShlAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return lhs.assign(fun.gen_bit_shl(lhs, self._rhs.gen_fun_value(fun)))
