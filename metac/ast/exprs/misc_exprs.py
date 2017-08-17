
from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode

class PtrExprNode(UnaryExprNode):
    pass


class DotExprNode(BinaryExprNode):
    pass

class InitExprNode(BinaryExprNode):
    pass

class AssignExprNode(BinaryExprNode):
    pass

class CallExprNode(ExprNode):
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args


class TernaryConditionalNode(ExprNode):
    def __init__(self, lhs, condition, rhs):
        self.lhs = lhs
        self.condition = condition
        self.rhs = rhs
