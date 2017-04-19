
from ...err import Todo

from ...ir import SymbolTable

class StatementNode:
    def hoist_unit_code(self, unit):
        pass

    def hoist_fun_code(self, block):
        pass

class BlockNode(StatementNode):
    def __init__(self, statements=None):
        self._statements = statements

    def hoist_unit_code(self, unit):
        self._symbols = SymbolTable(unit.symbols)
        unit.symbols = self._symbols

        for statement in self._statements:
            statement.hoist_unit_code(unit)

        unit.symbols = self._symbols.parent

    def gen_unit_code(self, unit):
        unit.symbols = self._symbols

        for statement in self._statements:
            statement.gen_unit_code(unit)

        unit.symbols = self._symbols.parent


    def hoist_fun_code(self, fun):
        self._symbols = SymbolTable(fun.symbols)
        fun.symbols = self._symbols

        for statement in self._statements:
            statement.hoist_fun_code(fun)

        fun.symbols = self._symbols.parent

    def gen_fun_code(self, fun):
        fun.symbols = self._symbols

        for statement in self._statements:
            statement.gen_fun_code(fun)

        fun.symbols = self._symbols.parent


class ReturnNode(StatementNode):
    def __init__(self, expr):
        self._expr = expr

    def hoist_fun_code(self, fun):
        self._expr.hoist_fun_code(fun)

    def gen_fun_code(self, fun):
        fun.create_return(self._expr.gen_fun_value(fun))
