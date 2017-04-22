
from ...err import Todo

from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode

class BitwiseAndExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()

class BitwiseXorExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()

class BitwiseOrExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()

class BitwiseNotExprNode(UnaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()


class ShrExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()

class ShlExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        raise Todo()
