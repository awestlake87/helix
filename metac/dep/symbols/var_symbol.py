
from ..target import Target

class VarTarget(Target):
    def _build_target(self):
        pass

class VarSymbol:
    def __init__(self):
        self._target = None

    def get_target(self):
        if self._target is None:
            self._target = VarTarget()

        return self._target
