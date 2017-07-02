
from ..symbol import Symbol
from ..targets import StructTarget

class StructSymbol(Symbol):
    def __init__(self, id):
        self._id = id
        self._target = StructTarget(self._id)

    def get_call_deps(self, scope, args):
        return [ self.get_target() ]

    def is_struct(self):
        return True

    def get_target(self):
        return self._target

    def __repr__(self):
        return "struct"
