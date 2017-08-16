

from ..ast import *
from ..err import Todo

from .types import *
from .values import *

def gen_static_expr_ir(scope, expr):
    expr_type = type(expr)

    if expr_type is IntTypeNode:
        return IntType(expr.num_bits, expr.is_signed)

    if expr_type is AutoIntNode:
        return IntValue(AutoIntType(), int(str(expr.value), expr.radix))

    if expr_type is IntNode:
        return IntValue(
            IntType(expr.num_bits, expr.is_signed),
            int(str(expr.value), expr.radix)
        )

    else:
        raise Todo(expr)

def gen_expr_ir(ctx, expr):
    expr_type = type(expr)

    if expr_type is CallExprNode:
        return gen_call_ir(ctx, expr)

    elif expr_type is SymbolNode:
        return ctx.scope.resolve(expr.id).get_ir_value()

    else:
        return gen_static_expr_ir(ctx.scope, expr)

def gen_condition_ir(ctx, expr):
    expr_type = type(expr)

    return gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr))

def gen_as_bit_ir(ctx, value):
    val_type = type(value.type)

    if value.type == BitType():
        return value

    elif val_type is IntType:
        return gen_neq_ir(ctx, value, IntValue(value.type, 0))

    else:
        raise Todo()

def gen_implicit_cast_ir(ctx, value, ir_as_type):
    val_type = type(value.type)
    as_type = type(ir_as_type)

    if val_type is as_type or val_type == as_type:
        return value

    elif val_type is AutoIntType and as_type is IntType:
        return IntValue(ir_as_type, value.value)

    else:
        raise Todo(value)

def gen_assign_code(ctx, lhs, rhs):
    ctx.builder.store(rhs.get_llvm_value(), lhs.get_llvm_ptr())

def gen_call_ir(ctx, expr):
    lhs = gen_expr_ir(ctx, expr.lhs)

    if type(lhs) is FunValue:
        if len(expr.args) != len(lhs.type.param_types):
            raise Todo("arg length mismatch")

        ir_args = [
            (
                gen_implicit_cast_ir(
                    ctx, gen_expr_ir(ctx, arg_node), param_type
                ).get_llvm_value()
            )
            for arg_node, param_type in
            zip(expr.args, lhs.type.param_types)
        ]

        return LlvmValue(
            lhs.type.ret_type, ctx.builder.call(lhs.get_llvm_value(), ir_args)
        )

    else:
        raise Todo(lhs)

def _gen_fun_cmp(ctx, op, lhs, rhs):
    cmp_type = get_common_type(lhs.type, rhs.type)

    if issubclass(type(cmp_type), IntType):
        if cmp_type.is_signed:
            return LlvmValue(
                BitType(),
                ctx.builder.icmp_signed(
                    op,
                    gen_implicit_cast_ir(ctx, lhs, cmp_type).get_llvm_value(),
                    gen_implicit_cast_ir(ctx, rhs, cmp_type).get_llvm_value()
                )
            )
        else:
            return LlvmValue(
                BitType(),
                ctx.builder.icmp_unsigned(
                    op,
                    gen_implicit_cast_ir(ctx, lhs, cmp_type).get_llvm_value(),
                    gen_implicit_cast_ir(ctx, rhs, cmp_type).get_llvm_value()
                )
            )
    else:
        raise Todo()

def gen_ltn_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "<", lhs, rhs)

def gen_leq_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "<=", lhs, rhs)

def gen_gtn_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, ">", lhs, rhs)

def gen_geq_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, ">=", lhs, rhs)

def gen_eql_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "==", lhs, rhs)

def gen_neq_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "!=", lhs, rhs)
