
from ...err import Todo

from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode


class AddExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()

class SubExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()

class MulExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()

class DivExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()

class ModExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()



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
