
from ..expr_sym import ExprSym

class SymbolSym(ExprSym):
    def __init__(self, id):
        self.id = id

class AutoIntSym(ExprSym):
    def __init__(self, value, radix):
        self.value = value
        self.radix = radix

class IntSym(ExprSym):
    def __init__(self, num_bits, is_signed, value, radix):
        self.num_bits = num_bits
        self.is_signed = is_signed
        self.value = str(value)
        self.radix = radix
        self.is_signed = is_signed
