
from ..err import Todo

from ..ir import SymbolTable

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

class IfStatementNode(StatementNode):
    def __init__(self, if_branches, else_block=None):
        self._if_branches = if_branches
        self._else_block = else_block

    def gen_fun_code(self, fun):
        assert len(self._if_branches) >= 1

        end_if = None

        def get_end_if():
            nonlocal end_if

            if end_if != None:
                return end_if
            else:
                end_if = fun._builder.append_basic_block("end_if")
                return end_if

        then_block = fun._builder.append_basic_block("then")
        else_block = fun._builder.append_basic_block("else")

        num = len(self._if_branches)

        for branch in self._if_branches:
            condition, block = branch

            fun._builder.cbranch(
                condition.gen_fun_value(fun).get_llvm_rval(fun._builder),
                then_block,
                else_block
            )

            with fun._builder.goto_block(then_block):
                block.hoist_fun_code(fun)
                block.gen_fun_code(fun)

            if not then_block.is_terminated:
                with fun._builder.goto_block(then_block):
                    fun._builder.branch(get_end_if())

            assert then_block.is_terminated

            fun._builder.position_at_start(else_block)

            if not branch is self._if_branches[-1]:
                then_block = fun._builder.append_basic_block("then")
                else_block = fun._builder.append_basic_block("else")

        if self._else_block != None:
            self._else_block.hoist_fun_code(fun)
            self._else_block.gen_fun_code(fun)
        else:
            fun._builder.branch(get_end_if())

        if not else_block.is_terminated:
            with fun._builder.goto_block(else_block):
                fun._builder.branch(get_end_if())

        assert else_block.is_terminated

        if end_if != None:
            fun._builder.position_at_start(get_end_if())

        assert end_if == None or not end_if.is_terminated
