
from ..err import Todo

class StatementNode:
    def hoist_unit_code(self, unit):
        pass

    def hoist_fun_code(self, block):
        pass

class BlockNode(StatementNode):
    def __init__(self, statements=None):
        self._statements = statements

    def hoist_unit_code(self, unit):
        for statement in self._statements:
            statement.hoist_unit_code(unit)

    def gen_unit_code(self, unit):
        for statement in self._statements:
            statement.gen_unit_code(unit)


    def hoist_fun_code(self, block):
        for statement in self._statements:
            statement.hoist_fun_code(block)

    def gen_fun_code(self, block):
        for statement in self._statements:
            statement.gen_fun_code(block)


class ReturnNode(StatementNode):
    def __init__(self, expr):
        self._expr = expr

    def hoist_fun_code(self, fun):
        self._expr.hoist_fun_code(fun)

    def gen_fun_code(self, fun):
        fun.create_return(self._expr.gen_fun_value(fun))

class IfStatementNode(StatementNode):
    def __init__(self, if_branches, else_block=None):
        self._if_branches = if_branches
        self._else_block = else_block

    def gen_fun_code(self, block):
        raise Todo()
