from ..statement_node import StatementNode

from ...err import Todo
from ...ir import SymbolTable

class LoopStatementNode(StatementNode):
    def __init__(
        self,
        for_clause,
        each_clause,
        while_clause,
        loop_body,
        then_clause,
        until_clause
    ):
        self._for_clause = for_clause
        self._each_clause = each_clause
        self._while_clause = while_clause
        self._loop_body = loop_body
        self._then_clause = then_clause
        self._until_clause = until_clause

    def gen_fun_code(self, fun):
        iter_symbols = SymbolTable(fun.symbols)
        body_symbols = SymbolTable(iter_symbols)

        if self._for_clause != None:
            with fun.using_scope(iter_symbols):
                self._for_clause.gen_fun_code(fun)

        if self._each_clause != None:
            raise Todo("each clause")


        loop_head = None
        loop_body = fun._builder.append_basic_block("loop_body")
        loop_exit = fun._builder.append_basic_block("loop_exit")

        if self._while_clause:
            loop_head = fun._builder.append_basic_block("loop_head")

            with fun._builder.goto_block(loop_head):
                with fun.using_scope(iter_symbols):
                    fun._builder.cbranch(
                        self._while_clause.gen_fun_value(fun).get_llvm_rval(),
                        loop_body,
                        loop_exit
                    )
        else:
            loop_head = loop_body

        fun._builder.branch(loop_head)

        with fun._builder.goto_block(loop_body):
            with fun.using_scope(body_symbols):
                self._loop_body.hoist_fun_code(fun)
                self._loop_body.gen_fun_code(fun)

            if self._then_clause != None:
                with fun.using_scope(iter_symbols):
                    self._then_clause.gen_fun_code(fun)

            if self._until_clause != None:
                raise Todo("until clause")

            fun._builder.branch(loop_head)

        fun._builder.position_at_start(loop_exit)
