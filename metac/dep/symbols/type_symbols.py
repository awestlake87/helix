
from ..symbol import Symbol

from llvmlite import ir

class IntTypeSymbol(Symbol):
    def get_mangled_name(self):
        return "i"

    def get_ir_type(self):
        return ir.IntType(32)
