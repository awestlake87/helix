
from ..target import Target

from ...err import Todo

class VarTarget(Target):
    def _build_target(self):
        pass

class VarSymbol:
    def __init__(self):
        self._target = None
        self._ir_value = None

    def get_target(self):
        if self._target is None:
            self._target = VarTarget()

        return self._target

    def set_ir_value(self, value):
        if self._ir_value is None:
            self._ir_value = value

        else:
            raise Todo("var has a value already")

    def get_ir_value(self):
        if self._ir_value is None:
            raise Todo("var has no value")

        else:
            return self._ir_value
