
from ..target import *

class UnitTarget(Target):
    def __init__(self, id, parent_scope, deps):
        self._id = id
        self._parent_scope = parent_scope

        super().__init__(deps)

    def _build_target(self):
        print(
            "build unit {}".format(
                self._parent_scope.get_qualified_name(self._id)
                if self._parent_scope else
                self._id
            )
        )
