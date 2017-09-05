
from ..expr_sym import *

class CallSym(ExprSym):
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args



class LtnSym(BinarySym):
    pass

class GtnSym(BinarySym):
    pass

class LeqSym(BinarySym):
    pass

class GeqSym(BinarySym):
    pass

class EqlSym(BinarySym):
    pass

class NeqSym(BinarySym):
    pass



class AndSym(BinarySym):
    pass

class OrSym(BinarySym):
    pass

class NotSym(UnarySym):
    pass

class XorSym(BinarySym):
    pass



class NegSym(UnarySym):
    pass



class PreIncSym(UnarySym):
    pass

class PostIncSym(UnarySym):
    pass

class PreDecSym(UnarySym):
    pass

class PostDecSym(UnarySym):
    pass



class BitAndSym(BinarySym):
    pass

class BitOrSym(BinarySym):
    pass

class BitNotSym(UnarySym):
    pass

class BitXorSym(BinarySym):
    pass

class BitShlSym(BinarySym):
    pass

class BitShrSym(BinarySym):
    pass



class InitSym(BinarySym):
    pass

class AssignSym(BinarySym):
    pass
