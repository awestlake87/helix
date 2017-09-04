

class ExprSym:
    pass

class BinarySym(ExprSym):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class UnarySym(ExprSym):
    def __init__(self, operand):
        self.operand = operand
