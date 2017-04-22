
from ...err import Todo

from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode


class AddExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_add(
            self._lhs.gen_fun_value(fun), self._rhs.gen_fun_value(fun)
        )

class SubExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_sub(
            self._lhs.gen_fun_value(fun), self._rhs.gen_fun_value(fun)
        )

class MulExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_mul(
            self._lhs.gen_fun_value(fun), self._rhs.gen_fun_value(fun)
        )

class DivExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_div(
            self._lhs.gen_fun_value(fun), self._rhs.gen_fun_value(fun)
        )

class ModExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_mod(
            self._lhs.gen_fun_value(fun), self._rhs.gen_fun_value(fun)
        )



class AddAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return lhs.assign(fun.gen_add(lhs, self._rhs.gen_fun_value(fun)))

class SubAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return lhs.assign(fun.gen_sub(lhs, self._rhs.gen_fun_value(fun)))

class MulAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return lhs.assign(fun.gen_mul(lhs, self._rhs.gen_fun_value(fun)))

class DivAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return lhs.assign(fun.gen_div(lhs, self._rhs.gen_fun_value(fun)))

class ModAssignExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        lhs = self._lhs.gen_fun_value(fun)

        return lhs.assign(fun.gen_mod(lhs, self._rhs.gen_fun_value(fun)))



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
