
from ..symbol import Symbol
from ..targets import UnitTarget
from ..scope import Scope

class UnitSymbol(Symbol):
    def __init__(self, id, block_node, parent_scope=None):
        self._id = id
        self._block_node = block_node
        self._parent_scope = parent_scope

        self._scope = Scope(id, parent_scope)

        self._block_node.hoist(self._scope)

    def get_target(self):
        return UnitTarget(
            self._id,
            self._parent_scope,
            self._block_node.get_deps(self._scope)
        )

    def is_unit(self):
        return True
