
from ..expr_sym import ExprSym, UnaryExprSym, BinaryExprSym



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



class AddSym(BinaryExprSym):
    pass

class SubSym(BinaryExprSym):
    pass

class MulSym(BinaryExprSym):
    pass

class DivSym(BinaryExprSym):
    pass

class ModSym(BinaryExprSym):
    pass



class BitAndSym(BinaryExprSym):
    pass

class BitOrSym(BinaryExprSym):
    pass

class BitXorSym(BinaryExprSym):
    pass

class BitNotSym(BinaryExprSym):
    pass

class BitShlSym(BinaryExprSym):
    pass

class BitShrSym(BinaryExprSym):
    pass



class AndSym(BinaryExprSym):
    pass

class OrSym(BinaryExprSym):
    pass

class NotSym(UnaryExprSym):
    pass

class XorSym(BinaryExprSym):
    pass



class PtrSym(UnaryExprSym):
    pass

class RefSym(UnaryExprSym):
    pass

class MutSym(UnaryExprSym):
    pass

class DotSym(BinaryExprSym):
    pass

class IndexSym(BinaryExprSym):
    pass



class AsSym(BinaryExprSym):
    pass

class CastSym(BinaryExprSym):
    pass

class BitcastSym(BinaryExprSym):
    pass



class SizeofSym(UnaryExprSym):
    pass

class OffsetofSym(BinaryExprSym):
    pass

class TypeofSym(UnaryExprSym):
    pass

class InitSym(BinaryExprSym):
    pass

class AssignSym(BinaryExprSym):
    pass



class BangSym(UnaryExprSym):
    pass

class TropeSym(UnaryExprSym):
    pass



class CallSym(ExprSym):
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args

class EmbedCallSym(ExprSym):
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args


class TernaryConditionalSym(ExprSym):
    def __init__(self, lhs, condition, rhs):
        self.lhs = lhs
        self.condition = condition
        self.rhs = rhs
