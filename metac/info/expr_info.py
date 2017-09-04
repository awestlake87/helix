
class ExprInfo:
    pass

class BinaryInfo(ExprInfo):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class UnaryInfo(ExprInfo):
    def __init__(self, operand):
        self.operand = operand
