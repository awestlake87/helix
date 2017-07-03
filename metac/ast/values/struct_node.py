
from ...ir import StructType
from ...err import Todo

from ..expr_node import ExprNode
from ...dep import StructSymbol

class StructNode(ExprNode):
    def __init__(self, id, attrs = [ ]):
        self._id = id
        self._attrs = attrs

        self._symbol = None

    def hoist(self, scope):
        if not self._id is None:
            self._symbol = StructSymbol(self._id, self._attrs, scope)
            scope.insert(self._id, self._symbol)
        else:
            raise Todo()

    def get_deps(self, scope):
        return [ self._symbol.get_target() ]

    def gen_unit_value(self, unit):
        return unit.symbols.insert(
            self._id,
            StructType([
                (type.gen_unit_value(unit), id) for type, id in self._attrs
            ])
        )

    def gen_fun_value(self, fun):
        raise Todo()
