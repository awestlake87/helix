
from ...err import Todo

from ..target import Target

class VarTarget(Target):
    def __init__(self):
        super().__init__([ ])

    def build(self):
        pass

class VarSymbol:
    def __init__(self, sym_type = None):
        self._target = None
        self._ir_value = None

        self.type = sym_type

    @property
    def target(self):
        if self._target is None:
            self._target = VarTarget()

        return self._target

    @property
    def ir_value(self):
        if self._ir_value is None:
            raise Todo("var has no value")

        else:
            return self._ir_value

    @ir_value.setter
    def ir_value(self, value):
        if self._ir_value is None:
            self._ir_value = value

        else:
            raise Todo("var has a value already")
