
from ...err import Todo

from ..statement_node import StatementNode

from ...ir import gen_fun_return

class ReturnNode(StatementNode):
    def __init__(self, expr):
        self._expr = expr

    def gen_fun_code(self, fun):
        gen_fun_return(fun, self._expr.gen_fun_value(fun))
