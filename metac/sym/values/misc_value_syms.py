
from ..expr_sym import ExprSym

class SymbolSym(ExprSym):
    def __init__(self, id):
        self.id = id

class AutoIntSym(ExprSym):
    def __init__(self, value, radix):
        self.value = value
        self.radix = radix
