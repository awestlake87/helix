
class ExprSym:
    pass

class BinaryExprSym(ExprSym):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class UnaryExprSym(ExprSym):
    def __init__(self, operand):
        self.operand = operand
