
from ..symbol import Symbol

class FunTypeSymbol(Symbol):
    pass

class IntTypeSymbol(Symbol):
    def get_mangled_name(self):
        return "i"
