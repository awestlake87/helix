
from ..symbol import Symbol
from ..targets import UnitTarget
from ..scope import Scope

class UnitSymbol(Symbol):
    def __init__(self, block_node, parent_scope=None):
        self._scope = Scope(parent_scope)
        self._block_node = block_node

        self._block_node.hoist(self._scope)

    def get_scope(self):
        return self._scope

    def get_target(self):
        return UnitTarget(self._block_node.get_deps(self._scope))

    def is_unit(self):
        return True
