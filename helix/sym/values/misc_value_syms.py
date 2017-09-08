
from ..expr_sym import *

class SymbolSym(ExprSym):
    def __init__(self, id):
        self.id = id

class AutoIntSym(ExprSym):
    def __init__(self, value, radix=10):
        self.value = value
        self.radix = radix

class IntSym(ExprSym):
    def __init__(self, num_bits, is_signed, value, radix=10):
        self.num_bits = num_bits
        self.is_signed = is_signed
        self.value = str(value)
        self.radix = radix
        self.is_signed = is_signed

class NilSym(ExprSym):
    pass

class AttrSym(ExprSym):
    def __init__(self, id):
        self.id = id

class StringSym(ExprSym):
    def __init__(self, value):
        self.value = value

class GlobalSym(ExprSym):
    def __init__(self, type_expr, id, is_cglobal=False):
        self.type = type_expr
        self.id = id
        self.is_cglobal = is_cglobal
