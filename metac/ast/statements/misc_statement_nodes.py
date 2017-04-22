
from ...err import Todo

from ..statement_node import StatementNode

class ReturnNode(StatementNode):
    def __init__(self, expr):
        self._expr = expr

    def hoist_fun_code(self, fun):
        self._expr.hoist_fun_code(fun)

    def gen_fun_code(self, fun):
        fun.create_return(self._expr.gen_fun_value(fun))
