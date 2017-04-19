
from ..err import SymbolNotFound, SymbolAlreadyExists

class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self._table = { }

    def has(self, id):
        if self.has_local(id):
            return True
        elif self.parent:
            return self.parent.has(id)
        else:
            return False

    def has_local(self, id):
        if id in self._table:
            return True
        else:
            return False

    def insert(self, id, value):
        if not self.has_local(id):
            self._table[id] = value
        else:
            raise SymbolAlreadyExists(id)

        return value

    def resolve(self, id):
        if self.has_local(id):
            return self._table[id]
        elif self.parent != None:
            return self.parent.resolve(id)
        else:
            raise SymbolNotFound(id)
