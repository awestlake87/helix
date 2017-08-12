
from ...err import Todo

from ..statement_node import StatementNode

from ...ir import gen_fun_return

class ReturnNode(StatementNode):
    def __init__(self, expr):
        self._expr = expr

    def hoist(self, scope):
        self._expr.hoist(scope)

    def get_deps(self, scope):
        return self._expr.get_deps(scope)

    def gen_code(self, fun, scope):
        raise Todo()

    def gen_fun_code(self, fun):
        gen_fun_return(fun, self._expr.gen_fun_value(fun))
