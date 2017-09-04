
class ExprInfo:
    pass

class BinaryExprInfo(ExprInfo):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class UnaryExprInfo(ExprInfo):
    def __init__(self, operand):
        self.operand = operand
