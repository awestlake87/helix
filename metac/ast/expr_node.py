from .statement_node import StatementNode

class ExprNode(StatementNode):
    pass

class UnaryNode(ExprNode):
    def __init__(self, operand):
        self.operand = operand

class BinaryNode(ExprNode):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
