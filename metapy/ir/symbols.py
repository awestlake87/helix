
from ..err import SymbolNotFound, SymbolAlreadyExists

class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self._table = { }

    def insert(self, id, value):
        if not id in self._table:
            self._table[id] = value
        else:
            raise SymbolAlreadyExists(id)

        return value

    def resolve(self, id):
        if id in self._table:
            return self._table[id]
        elif self.parent != None:
            return self.parent.resolve(id)
        else:
            raise SymbolNotFound(id)
