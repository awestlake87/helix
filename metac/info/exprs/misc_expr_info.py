from ..expr_info import *

class CallInfo:
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args

class EmbedCallInfo:
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args



class LtnInfo(BinaryExprInfo):
    pass

class GtnInfo(BinaryExprInfo):
    pass

class LeqInfo(BinaryExprInfo):
    pass

class GeqInfo(BinaryExprInfo):
    pass

class EqlInfo(BinaryExprInfo):
    pass

class NeqInfo(BinaryExprInfo):
    pass



class AndInfo(BinaryExprInfo):
    pass

class OrInfo(BinaryExprInfo):
    pass

class NotInfo(UnaryExprInfo):
    pass

class XorInfo(BinaryExprInfo):
    pass



class AddInfo(BinaryExprInfo):
    pass

class SubInfo(BinaryExprInfo):
    pass

class MulInfo(BinaryExprInfo):
    pass

class DivInfo(BinaryExprInfo):
    pass

class ModInfo(BinaryExprInfo):
    pass



class BitAndInfo(BinaryExprInfo):
    pass

class BitOrInfo(BinaryExprInfo):
    pass

class BitNotInfo(UnaryExprInfo):
    pass

class BitXorInfo(BinaryExprInfo):
    pass

class BitShlInfo(BinaryExprInfo):
    pass

class BitShrInfo(BinaryExprInfo):
    pass



class PreIncInfo(UnaryExprInfo):
    pass

class PostIncInfo(UnaryExprInfo):
    pass

class PreDecInfo(UnaryExprInfo):
    pass

class PostDecInfo(UnaryExprInfo):
    pass



class PtrExprInfo(UnaryExprInfo):
    pass

class RefExprInfo(UnaryExprInfo):
    pass



class InitInfo(BinaryExprInfo):
    pass

class AssignInfo(BinaryExprInfo):
    pass

class DotInfo(BinaryExprInfo):
    pass

class OffsetofInfo(UnaryExprInfo):
    pass

class TernaryConditionalInfo:
    pass
