
from ..err import Todo

from .values import UnitSymbol

def gen_unit_sym(unit_node):
    return UnitSymbol(unit_node.id, unit_node)
