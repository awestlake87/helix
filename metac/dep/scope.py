
import json

from ..err import SymbolNotFound, SymbolAlreadyExists

class Scope:
    def __init__(self, id, parent=None):
        self._id = id
        self._parent = parent
        self._symbols = { }

    def to_dict(self):
        symbol_dict = { }

        for id, symbol in self._symbols.items():
            scope = symbol.get_scope()

            if type(scope) is Scope:
                symbol_dict[id] = scope.to_dict()
            else:
                symbol_dict[id] = scope

        return symbol_dict

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

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

    def get_scope_name(self):
        if self._id and self._parent:
            return "{}/{}".format(self._parent.get_scope_name(), self._id)
        elif self._id:
            return self._id
        elif self._parent:
            return self._parent.get_scope_name()
        else:
            return ""

    def get_qualified_name(self, id):
        if self.has_local(id):
            return "{}/{}".format(self.get_scope_name(), id)
        elif self._parent:
            return self._parent.get_qualified_name(id)
        else:
            raise SymbolNotFound(id)
