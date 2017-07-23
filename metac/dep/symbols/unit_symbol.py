
from ..symbol import Symbol
from ..scope import Scope

from .fun_symbols import FunTarget

from ..target import *

class UnitTarget(Target):
    def __init__(self, id, parent_scope, deps):
        self._id = id
        self._parent_scope = parent_scope

        super().__init__(deps)

    def _get_target_name(self):
        return "unit {}".format(
            self._parent_scope.get_qualified_name(self._id)
            if self._parent_scope else
            self._id
        )

    def _build_target(self):
        for target in self._deps:
            if type(target) is FunTarget:
                print(
                    "link {} into {}".format(
                        target._id, self._get_target_name()
                    )
                )


class UnitSymbol(Symbol):
    def __init__(self, id, block_node, parent_scope=None):
        self._id = id
        self._block_node = block_node
        self._parent_scope = parent_scope

        self._scope = Scope(id, parent_scope)

        self._block_node.hoist(self._scope)

        self._target = None

    def get_target(self):
        if not self._target:
            self._target = UnitTarget(
                self._id,
                self._parent_scope,
                self._block_node.get_deps(self._scope)
            )

        return self._target

    def is_unit(self):
        return True
