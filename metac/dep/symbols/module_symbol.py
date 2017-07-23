
from .unit_symbol import UnitSymbol
from ..scope import Scope

class ModuleSymbol:
    def __init__(self, id, global_scope):
        self._scope = Scope(id, global_scope)
        self._entry = None

    def set_entry(self, block):
        self._entry = UnitSymbol("index", block, self._scope)
        self._scope.insert("index", self._entry)

    def get_target(self):
        return self._entry.get_target()
