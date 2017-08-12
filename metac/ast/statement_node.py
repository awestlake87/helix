
from .node import Node
from ..err import Todo

class StatementNode(Node):
    def gen_code(self, fun, scope):
        raise Todo()

    def hoist_unit_code(self, unit):
        pass

    def hoist_fun_code(self, block):
        pass
