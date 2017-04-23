
from .expr_node import BinaryExprNode, UnaryExprNode

from ..err import Todo
from ..ir import IntType, FunLlvmRVal

import llvmlite

class AndNode(BinaryExprNode):
    def gen_unit_value(self, unit):
        raise Todo()

    def gen_fun_value(self, fun):
        and_lhs_true = fun._builder.append_basic_block("and_lhs_true")
        and_true = fun._builder.append_basic_block("and_true")
        and_false = fun._builder.append_basic_block("and_false")
        and_end = fun._builder.append_basic_block("and_end")

        fun._builder.cbranch(
            self._lhs.gen_fun_value(fun).as_bit().get_llvm_rval(),
            and_lhs_true,
            and_false
        )

        fun._builder.position_at_start(and_end)
        phi = fun._builder.phi(IntType(1, False).get_llvm_type())

        with fun._builder.goto_block(and_lhs_true):
            fun._builder.cbranch(
                self._rhs.gen_fun_value(fun).as_bit().get_llvm_rval(),
                and_true,
                and_false
            )

        with fun._builder.goto_block(and_true):
            phi.add_incoming(
                llvmlite.ir.IntType(1)(1),
                and_true
            )
            fun._builder.branch(and_end)

        with fun._builder.goto_block(and_false):
            phi.add_incoming(
                llvmlite.ir.IntType(1)(0),
                and_false
            )
            fun._builder.branch(and_end)

        return FunLlvmRVal(fun, IntType(1, False), phi)

class XorNode(BinaryExprNode):
    def gen_unit_value(self, unit):
        raise Todo()

    def gen_fun_value(self, fun):
        return fun.gen_bit_xor(
            self._lhs.gen_fun_value(fun).as_bit(),
            self._rhs.gen_fun_value(fun).as_bit()
        )

class OrNode(BinaryExprNode):
    def gen_unit_value(self, unit):
        raise Todo()

    def gen_fun_value(self, fun):
        or_lhs_false = fun._builder.append_basic_block("or_lhs_false")
        or_true = fun._builder.append_basic_block("or_true")
        or_false = fun._builder.append_basic_block("or_false")
        or_end = fun._builder.append_basic_block("or_end")

        fun._builder.cbranch(
            self._lhs.gen_fun_value(fun).as_bit().get_llvm_rval(),
            or_true,
            or_lhs_false
        )

        fun._builder.position_at_start(or_end)
        phi = fun._builder.phi(IntType(1, False).get_llvm_type())

        with fun._builder.goto_block(or_lhs_false):
            fun._builder.cbranch(
                self._rhs.gen_fun_value(fun).as_bit().get_llvm_rval(),
                or_true,
                or_false
            )

        with fun._builder.goto_block(or_true):
            phi.add_incoming(
                llvmlite.ir.IntType(1)(1),
                or_true
            )
            fun._builder.branch(or_end)

        with fun._builder.goto_block(or_false):
            phi.add_incoming(
                llvmlite.ir.IntType(1)(0),
                or_false
            )
            fun._builder.branch(or_end)

        return FunLlvmRVal(fun, IntType(1, False), phi)

class NotNode(UnaryExprNode):
    def gen_unit_value(self, unit):
        raise Todo()

    def gen_fun_value(self, fun):
        return fun.gen_bit_not(
            self._operand.gen_fun_value(fun).as_type(IntType(1, False))
        )


class LtnExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_ltn(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class GtnExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_gtn(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class LeqExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_leq(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )

class GeqExprNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_geq(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )


class EqNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_eq(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )
class NeqNode(BinaryExprNode):
    def gen_fun_value(self, fun):
        return fun.gen_neq(
            self._lhs.gen_fun_value(fun),
            self._rhs.gen_fun_value(fun)
        )
