
from ...ir import (
    PtrType,
    Type,
    get_common_type,
    get_concrete_type,
    FunLlvmRVal,
    IntType,
    gen_fun_call,
    gen_fun_as_bit,
    gen_fun_as,
    gen_fun_assign,
    gen_fun_dot
)

from ...err import Todo

from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode
from ..values import SymbolNode

class PtrExprNode(UnaryExprNode):
    def gen_unit_value(self, unit):
        value = self._operand.gen_unit_value(unit)

        if value.is_type():
            return PtrType(value)
        else:
            raise Todo("dereferencing values")


class DotExpr(BinaryExprNode):
    def gen_fun_value(self, fun):
        if type(self._rhs) is SymbolNode:
            return gen_fun_dot(
                fun,
                self._lhs.gen_fun_value(fun),
                self._rhs._id
            )

        else:
            raise Todo()

class InitExprNode(BinaryExprNode):
    def gen_unit_value(self, unit):
        raise Todo()

    def gen_fun_value(self, fun):
        if type(self._lhs) is SymbolNode:
            value = self._rhs.gen_fun_value(fun)
            return fun.symbols.insert(
                self._lhs._id,
                gen_fun_assign(
                    fun,
                    fun.create_stack_var(value.type),
                    value
                )
            )
        else:
            raise Todo()

class AssignExprNode(BinaryExprNode):
    def gen_unit_value(self, unit):
        raise Todo()

    def gen_fun_value(self, fun):
        return gen_fun_assign(
            fun,
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class CallExprNode(ExprNode):
    def __init__(self, lhs, args):
        self._lhs = lhs
        self._args = args

    def hoist(self, scope):
        self._lhs.hoist(scope)

        for arg in self._args:
            arg.hoist(scope)

    def get_deps(self, scope):
        targets = [ ]
        targets += self._lhs.get_deps(scope)

        for arg in self._args:
            targets += arg.get_deps(scope)

        targets += self._lhs.get_value(scope).get_call_deps(
            scope, self._args
        )

        return targets


    def gen_unit_value(self, unit):
        return self._lhs.gen_unit_value(unit).call(
            unit, [ arg.gen_unit_value(unit) for arg in self._args ]
        )

    def gen_fun_value(self, fun):
        return gen_fun_call(
            fun,
            self._lhs.gen_fun_value(fun),
            [ arg.gen_fun_value(fun) for arg in self._args ]
        )


class TernaryConditionalNode(ExprNode):
    def __init__(self, lhs, condition, rhs):
        self._lhs = lhs
        self._condition = condition
        self._rhs = rhs

    def gen_fun_value(self, fun):
        tern_true = fun._builder.append_basic_block("tern_true")
        tern_false = fun._builder.append_basic_block("tern_false")
        tern_end = fun._builder.append_basic_block("tern_end")

        fun._builder.cbranch(
            gen_fun_as_bit(
                fun,
                self._condition.gen_fun_value(fun)
            ).get_llvm_rval(),
            tern_true,
            tern_false
        )

        lhs_value = None
        rhs_value = None

        with fun._builder.goto_block(tern_true):
            lhs_value = self._lhs.gen_fun_value(fun)
            fun._builder.branch(tern_end)

        with fun._builder.goto_block(tern_false):
            rhs_value = self._rhs.gen_fun_value(fun)
            fun._builder.branch(tern_end)

        val_type = get_concrete_type(
            get_common_type(lhs_value.type, rhs_value.type)
        )

        if type(val_type) is IntType:
            fun._builder.position_at_start(tern_end)

            phi = fun._builder.phi(val_type.get_llvm_type())

            phi.add_incoming(
                gen_fun_as(fun, lhs_value, val_type).get_llvm_rval(),
                tern_true
            )
            phi.add_incoming(
                gen_fun_as(fun, rhs_value, val_type).get_llvm_rval(),
                tern_false
            )

            return FunLlvmRVal(fun, val_type, phi)

        else:
            raise Todo()
