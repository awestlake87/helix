from .statement_node import StatementNode

class ExprNode(StatementNode):
    pass

class UnaryExprNode(ExprNode):
    def __init__(self, operand):
        self.operand = operand

class BinaryExprNode(ExprNode):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
