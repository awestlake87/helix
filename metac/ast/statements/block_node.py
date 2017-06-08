
from ...ir import SymbolTable

from ..statement_node import StatementNode

from ...dep import Scope

class BlockNode(StatementNode):
    def __init__(self, statements=[ ]):
        self._statements = statements

    def hoist(self, scope):
        for statement in self._statements:
            statement.hoist(scope)

    def create_targets(self, scope):
        targets = [ ]

        for statement in self._statements:
            targets += statement.create_targets(scope)

        return targets

    def is_empty(self):
        return len(self._statements) == 0

    def hoist_unit_code(self, unit):
        self._symbols = SymbolTable(unit.symbols)

        with unit.using_scope(self._symbols):
            for statement in self._statements:
                statement.hoist_unit_code(unit)

    def gen_unit_code(self, unit):
        with unit.using_scope(self._symbols):
            for statement in self._statements:
                statement.gen_unit_code(unit)


    def hoist_fun_code(self, fun):
        self._symbols = SymbolTable(fun.symbols)

        with fun.using_scope(self._symbols):
            for statement in self._statements:
                statement.hoist_fun_code(fun)

    def gen_fun_code(self, fun):
        with fun.using_scope(self._symbols):
            for statement in self._statements:
                statement.gen_fun_code(fun)
