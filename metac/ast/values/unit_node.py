
from ...ir import Unit
from ...err import Todo

from ..expr_node import ExprNode

from ...dep import UnitSymbol

class UnitNode(ExprNode):
    def __init__(self, id, block):
        self._block = block
        self._symbol = UnitSymbol(id, self._block)

    def get_symbol(self):
        return self._symbol

    def gen_module_value(self, module):
        unit = Unit()

        self._block.hoist_unit_code(unit)
        self._block.gen_unit_code(unit)

        return unit
