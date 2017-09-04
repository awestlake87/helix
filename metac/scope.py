
import json

from .err import SymbolNotFound, SymbolAlreadyExists

class Scope:
    def __init__(self, parent=None):
        self._parent = parent
        self._symbols = { }

    def insert(self, id, target):
        if not self.has_local(id):
            self._symbols[id] = target
        else:
            raise SymbolAlreadyExists(id)

    def has_local(self, id):
        if id in self._symbols:
            return True
        else:
            return False

    def resolve(self, id):
        if self.has_local(id):
            return self._symbols[id]
        elif self._parent:
            return self._parent.resolve(id)
        else:
            raise SymbolNotFound(id)
