from contextlib import contextmanager

from ...err import ReturnTypeMismatch, NotApplicable, Todo
from ..symbols import SymbolTable
from .values import Value, ConstLlvmValue, StackValue, StaticValue, LlvmRVal
from ..types import AutoIntType, IntType, get_common_type, get_concrete_type

from llvmlite import ir

class Fun(Value):
    EXTERN_C = 0
    INTERN_C = 1

    def __init__(self, unit, type, id, param_ids, linkage):
        self.unit = unit
        self.type = type

        self._builder = None
        self._id = id
        self._fun = ir.Function(
            unit._module, self.type.get_llvm_type(), id
        )

        for arg, id in zip(self._fun.args, param_ids):
            arg.name = id

        if linkage == Fun.EXTERN_C:
            self._fun.linkage = "external"

        elif linkage == Fun.INTERN_C:
            self._fun.linkage = "internal"

    def create_body(self):
        self._entry = self._fun.append_basic_block("entry")

        self._builder = ir.IRBuilder(self._entry)

        self._body = self._builder.append_basic_block("body")
        self._builder.branch(self._body)
        self._builder.position_at_end(self._body)

        self.symbols = SymbolTable(self.unit.symbols)

        for type, arg in zip(self.type._param_types, self._fun.args):
            self.symbols.insert(arg.name, ConstLlvmValue(type, arg))

    def call(self, fun, args):
        if len(args) != len(self.type._param_types):
            raise Todo("arg length mismatch")

        llvm_args = [ ]

        for type, arg in zip(self.type._param_types, args):
            if arg.type.can_convert_to(type):
                arg_value = arg.as_type(type)
                llvm_args.append(arg_value.get_llvm_rval())

            else:
                raise NotApplicable()

        return ConstLlvmValue(
            self.type._ret_type, fun._builder.call(self._fun, llvm_args)
        )

    def create_return(self, value):
        if value.type.can_convert_to(self.type._ret_type):
            ret_value = value.as_type(self.type._ret_type)
            self._builder.ret(ret_value.get_llvm_rval())

        else:
            raise ReturnTypeMismatch()

    def create_stack_var(self, ir_type):
        llvm_value = None

        if type(ir_type) is AutoIntType:
            with self._builder.goto_block(self._entry):
                var_type = IntType()
                llvm_value = self._builder.alloca(
                    var_type.get_llvm_type()
                )

                return StackValue(self, var_type, llvm_value)

        else:
            with self._builder.goto_block(self._entry):
                llvm_value = self._builder.alloca(
                    ir_type.get_llvm_type()
                )

                return StackValue(self, ir_type, llvm_value)

    def gen_pre_inc(self, operand):
        if not operand.is_lval():
            raise NotApplicable()

        op_type = get_concrete_type(operand.type)

        if type(op_type) is IntType:
            return operand.assign(
                LlvmRVal(
                    op_type,
                    self._builder.add(
                        operand.as_type(op_type).get_llvm_rval(),
                        StaticValue(op_type, 1).get_llvm_rval()
                    )
                )
            )

        else:
            raise Todo()

    def gen_post_inc(self, operand):
        if not operand.is_lval():
            raise NotApplicable()

        op_type = get_concrete_type(operand.type)

        if type(op_type) is IntType:
            value = LlvmRVal(
                op_type,
                operand.as_type(op_type).get_llvm_rval()
            )

            operand.assign(
                LlvmRVal(
                    op_type,
                    self._builder.add(
                        value.get_llvm_rval(),
                        StaticValue(op_type, 1).get_llvm_rval()
                    )
                )
            )

            return value

        else:
            raise Todo()

    def gen_pre_dec(self, operand):
        if not operand.is_lval():
            raise NotApplicable()

        op_type = get_concrete_type(operand.type)

        if type(op_type) is IntType:
            return operand.assign(
                LlvmRVal(
                    op_type,
                    self._builder.sub(
                        operand.as_type(op_type).get_llvm_rval(),
                        StaticValue(op_type, 1).get_llvm_rval()
                    )
                )
            )

        else:
            raise Todo()

    def gen_post_dec(self, operand):
        if not operand.is_lval():
            raise NotApplicable()

        op_type = get_concrete_type(operand.type)

        if type(op_type) is IntType:
            value = LlvmRVal(
                op_type,
                operand.as_type(op_type).get_llvm_rval()
            )

            operand.assign(
                LlvmRVal(
                    op_type,
                    self._builder.sub(
                        value.get_llvm_rval(),
                        StaticValue(op_type, 1).get_llvm_rval()
                    )
                )
            )

            return value

        else:
            raise Todo()

    def gen_negate(self, operand):
        op_type = get_concrete_type(operand.type)

        if type(op_type) is IntType:
            return LlvmRVal(
                op_type,
                self._builder.neg(
                    operand.as_type(op_type).get_llvm_rval()
                )
            )

        else:
            raise Todo()

    def gen_add(self, lhs, rhs):
        common_type = get_common_type(lhs.type, rhs.type)

        if type(common_type) is IntType:
            return LlvmRVal(
                common_type,
                self._builder.add(
                    lhs.as_type(common_type).get_llvm_rval(),
                    rhs.as_type(common_type).get_llvm_rval()
                )
            )

        else:
            raise Todo()

    def gen_sub(self, lhs, rhs):
        common_type = get_common_type(lhs.type, rhs.type)

        if type(common_type) is IntType:
            return LlvmRVal(
                common_type,
                self._builder.sub(
                    lhs.as_type(common_type).get_llvm_rval(),
                    rhs.as_type(common_type).get_llvm_rval()
                )
            )

        else:
            raise Todo()

    def gen_mul(self, lhs, rhs):
        common_type = get_common_type(lhs.type, rhs.type)

        if type(common_type) is IntType:
            return LlvmRVal(
                common_type,
                self._builder.mul(
                    lhs.as_type(common_type).get_llvm_rval(),
                    rhs.as_type(common_type).get_llvm_rval()
                )
            )

        else:
            raise Todo()

    def gen_div(self, lhs, rhs):
        common_type = get_common_type(lhs.type, rhs.type)

        if type(common_type) is IntType:
            if common_type._is_signed:
                return LlvmRVal(
                    common_type,
                    self._builder.sdiv(
                        lhs.as_type(common_type).get_llvm_rval(),
                        rhs.as_type(common_type).get_llvm_rval()
                    )
                )
            else:
                return LlvmRVal(
                    common_type,
                    self._builder.udiv(
                        lhs.as_type(common_type).get_llvm_rval(),
                        rhs.as_type(common_type).get_llvm_rval()
                    )
                )

        else:
            raise Todo()

    def gen_mod(self, lhs, rhs):
        common_type = get_common_type(lhs.type, rhs.type)

        if type(common_type) is IntType:
            if common_type._is_signed:
                return LlvmRVal(
                    common_type,
                    self._builder.srem(
                        lhs.as_type(common_type).get_llvm_rval(),
                        rhs.as_type(common_type).get_llvm_rval()
                    )
                )
            else:
                return LlvmRVal(
                    common_type,
                    self._builder.urem(
                        lhs.as_type(common_type).get_llvm_rval(),
                        rhs.as_type(common_type).get_llvm_rval()
                    )
                )

        else:
            raise Todo()

    def gen_ltn(self, lhs, rhs):
        return self._gen_cmp("<", lhs, rhs)

    def gen_leq(self, lhs, rhs):
        return self._gen_cmp("<=", lhs, rhs)

    def gen_gtn(self, lhs, rhs):
        return self._gen_cmp(">", lhs, rhs)

    def gen_geq(self, lhs, rhs):
        return self._gen_cmp(">=", lhs, rhs)

    def gen_eq(self, lhs, rhs):
        return self._gen_cmp("==", lhs, rhs)

    def gen_neq(self, lhs, rhs):
        return self._gen_cmp("!=", lhs, rhs)


    def _gen_cmp(self, op, lhs, rhs):
        cmp_type = get_common_type(lhs.type, rhs.type)

        if type(cmp_type) is IntType:
            if cmp_type._is_signed:
                return LlvmRVal(
                    IntType(1, False),
                    self._builder.icmp_signed(
                        op,
                        lhs.as_type(cmp_type).get_llvm_rval(),
                        rhs.as_type(cmp_type).get_llvm_rval()
                    )
                )
            else:
                return LlvmRVal(
                    IntType(1, False),
                    self._builder.icmp_unsigned(
                        op,
                        lhs.as_type(cmp_type).get_llvm_rval(),
                        rhs.as_type(cmp_type).get_llvm_rval()
                    )
                )
        else:
            raise Todo()

    @contextmanager
    def using_scope(self, symbols):
        old_symbols = self.symbols
        self.symbols = symbols

        yield

        self.symbols = old_symbols

    def is_rval(self):
        return True

    def get_llvm_rval(self):
        return self._fun
