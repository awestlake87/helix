
from ..expr_sym import *

class CallExprSym(ExprSym):
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args



class LtnSym(BinaryExprSym):
    pass

class GtnSym(BinaryExprSym):
    pass

class LeqSym(BinaryExprSym):
    pass

class GeqSym(BinaryExprSym):
    pass

class EqlSym(BinaryExprSym):
    pass

class NeqSym(BinaryExprSym):
    pass



class PreIncExprSym(UnaryExprSym):
    pass

class PostIncExprSym(UnaryExprSym):
    pass

class PreDecExprSym(UnaryExprSym):
    pass

class PostDecExprSym(UnaryExprSym):
    pass



class InitExprSym(BinaryExprSym):
    pass

class AssignSym(BinaryExprSym):
    pass
