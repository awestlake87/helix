
from ..statement_node import StatementNode

class IfStatementNode(StatementNode):
    def __init__(self, if_branches, else_block=None):
        self._if_branches = if_branches
        self._else_block = else_block

    def gen_fun_code(self, fun):
        assert len(self._if_branches) >= 1

        end_if = fun._builder.append_basic_block("end_if")
        then_block = fun._builder.append_basic_block("then")
        else_block = fun._builder.append_basic_block("else")

        num = len(self._if_branches)

        for branch in self._if_branches:
            condition, block = branch

            fun._builder.cbranch(
                condition.gen_fun_value(fun).get_llvm_rval(),
                then_block,
                else_block
            )

            with fun._builder.goto_block(then_block):
                block.hoist_fun_code(fun)
                block.gen_fun_code(fun)

                if not fun._builder.block.is_terminated:
                    fun._builder.branch(end_if)

            assert then_block.is_terminated

            fun._builder.position_at_start(else_block)

            if not branch is self._if_branches[-1]:
                then_block = fun._builder.append_basic_block("then")
                else_block = fun._builder.append_basic_block("else")


        with fun._builder.goto_block(else_block):
            if self._else_block != None:
                self._else_block.hoist_fun_code(fun)
                self._else_block.gen_fun_code(fun)

                if not fun._builder.block.is_terminated:
                    fun._builder.branch(end_if)
            else:
                fun._builder.branch(end_if)

        assert else_block.is_terminated
        assert not end_if.is_terminated

        fun._builder.position_at_start(end_if)
