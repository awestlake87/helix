
from ...err import Todo
from ...ir import IntType, AutoIntType, gen_fun_as

from ..statement_node import StatementNode

class SwitchStatementNode(StatementNode):
    def __init__(self, value, case_branches = [ ], default_block = None):
        self._value = value
        self._case_branches = case_branches
        self._default_block = default_block

    def hoist(self, scope):
        self._value.hoist(scope)

        for value, block in self._case_branches:
            value.hoist(scope)
            block.hoist(scope)

        if self._default_block:
            self._default_block.hoist(scope)

    def get_deps(self, scope):
        targets = [ ]

        targets += self._value.get_deps(scope)

        for value, block in self._case_branches:
            targets += value.get_deps(scope)
            targets += block.get_deps(scope)

        if self._default_block:
            targets += self._default_block.get_deps(scope)

        return targets

    def gen_code(self, fun, scope):
        raise Todo()

    def gen_unit_code(self, unit):
        raise Todo()

    def gen_fun_code(self, fun):
        llvm_default_block = fun._builder.append_basic_block("default")

        value = self._value.gen_fun_value(fun)

        if type(value.type) is AutoIntType:
            value = gen_fun_as(fun, value, IntType())


        if not type(value.type) is IntType:
            raise Todo("non-integer switches")

        inst = fun._builder.switch(
            value.get_llvm_rval(),
            llvm_default_block
        )

        for c in self._case_branches:
            case_value, case_block = c

            value = case_value.gen_fun_value(fun)
            block = fun._builder.append_basic_block("case")

            if not value.is_static():
                raise Todo("non-static cases?")

            if type(value.type) is AutoIntType:
                value = gen_fun_as(fun, value, IntType())

            inst.add_case(
                value.get_llvm_rval(),
                block
            )

            with fun._builder.goto_block(block):
                case_block.hoist_fun_code(fun)
                case_block.gen_fun_code(fun)


        with fun._builder.goto_block(llvm_default_block):
            self._default_block.hoist_fun_code(fun)
            self._default_block.gen_fun_code(fun)
