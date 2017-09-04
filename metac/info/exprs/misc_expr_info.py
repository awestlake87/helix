from ..expr_info import *

class CallInfo:
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args

class EmbedCallInfo:
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args



class LtnInfo(BinaryInfo):
    pass

class GtnInfo(BinaryInfo):
    pass

class LeqInfo(BinaryInfo):
    pass

class GeqInfo(BinaryInfo):
    pass

class EqlInfo(BinaryInfo):
    pass

class NeqInfo(BinaryInfo):
    pass



class AndInfo(BinaryInfo):
    pass

class OrInfo(BinaryInfo):
    pass

class NotInfo(UnaryInfo):
    pass

class XorInfo(BinaryInfo):
    pass



class NegInfo(UnaryInfo):
    pass



class AddInfo(BinaryInfo):
    pass

class SubInfo(BinaryInfo):
    pass

class MulInfo(BinaryInfo):
    pass

class DivInfo(BinaryInfo):
    pass

class ModInfo(BinaryInfo):
    pass



class BitAndInfo(BinaryInfo):
    pass

class BitOrInfo(BinaryInfo):
    pass

class BitNotInfo(UnaryInfo):
    pass

class BitXorInfo(BinaryInfo):
    pass

class BitShlInfo(BinaryInfo):
    pass

class BitShrInfo(BinaryInfo):
    pass



class PreIncInfo(UnaryInfo):
    pass

class PostIncInfo(UnaryInfo):
    pass

class PreDecInfo(UnaryInfo):
    pass

class PostDecInfo(UnaryInfo):
    pass



class PtrExprInfo(UnaryInfo):
    pass

class RefExprInfo(UnaryInfo):
    pass



class InitInfo(BinaryInfo):
    pass

class AssignInfo(BinaryInfo):
    pass

class DotInfo(BinaryInfo):
    pass

class OffsetofInfo(UnaryInfo):
    pass

class TernaryConditionalInfo:
    pass
