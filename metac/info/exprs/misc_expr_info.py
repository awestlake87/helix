from ..expr_info import *

class CallExprInfo:
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args

class EmbedCallExprInfo:
    pass

class AndInfo:
    pass

class OrInfo:
    pass

class NotInfo:
    pass

class XorInfo:
    pass

class InitExprInfo:
    pass

class DotExprInfo:
    pass

class OffsetofInfo:
    pass

class TernaryConditionalInfo:
    pass
