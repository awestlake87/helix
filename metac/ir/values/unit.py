from contextlib import contextmanager
from llvmlite import ir

from .values import Value

from ..symbols import SymbolTable

class Unit(Value):
    def __init__(self):
        self._module = ir.Module("todo")
        self.symbols = SymbolTable()


    @contextmanager
    def using_scope(self, symbols):
        old_symbols = self.symbols
        self.symbols = symbols

        yield

        self.symbols = old_symbols
