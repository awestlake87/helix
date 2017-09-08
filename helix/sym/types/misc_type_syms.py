from ..expr_sym import ExprSym

class FunTypeSym(ExprSym):
    def __init__(self, ret_type, param_types):
        self.ret_type = ret_type
        self.param_types = param_types

class IntTypeSym(ExprSym):
    def __init__(self, num_bits, is_signed):
        self.num_bits = num_bits
        self.is_signed = is_signed

class ArrayTypeSym(ExprSym):
    def __init__(self, length, type_expr):
        self.length = length
        self.type = type_expr

class VoidTypeSym(ExprSym):
    pass

class AutoTypeSym(ExprSym):
    pass
