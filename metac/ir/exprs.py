

from ..ast import *
from ..err import Todo

from .types import *
from .values import *

def gen_static_expr_ir(scope, expr):
    expr_type = type(expr)

    if expr_type is PtrExprNode:
        return gen_static_ptr_expr_ir(scope, expr)

    elif expr_type is IntTypeNode:
        return IntType(expr.num_bits, expr.is_signed)

    elif expr_type is AutoIntNode:
        return IntValue(AutoIntType(), int(str(expr.value), expr.radix))

    elif expr_type is IntNode:
        return IntValue(
            IntType(expr.num_bits, expr.is_signed),
            int(str(expr.value), expr.radix)
        )

    elif expr_type is NilNode:
        return NilValue(AutoPtrType())

    else:
        raise Todo(expr)

def gen_static_ptr_expr_ir(scope, expr):
    pointee = gen_static_expr_ir(scope, expr.operand)

    if issubclass(type(pointee), Type):
        return PtrType(pointee)

    else:
        raise Todo(pointee)

def gen_expr_ir(ctx, expr):
    expr_type = type(expr)

    if expr_type is CallExprNode:
        return gen_call_ir(ctx, expr)

    elif expr_type is SymbolNode:
        return ctx.scope.resolve(expr.id).get_ir_value()

    elif expr_type is AndNode:
        return gen_and_ir(ctx, expr)

    elif expr_type is OrNode:
        return gen_or_ir(ctx, expr)

    elif expr_type is NotNode:
        return gen_not_ir(ctx, expr)

    elif expr_type is XorNode:
        return gen_xor_ir(ctx, expr)

    elif expr_type is InitExprNode:
        return gen_init_ir(ctx, expr)

    elif issubclass(expr_type, BinaryExprNode):
        return gen_binary_expr_ir(ctx, expr)

    else:
        return gen_static_expr_ir(ctx.scope, expr)

def gen_binary_expr_ir(ctx, expr):
    expr_type = type(expr)
    lhs = gen_expr_ir(ctx, expr.lhs)
    rhs = gen_expr_ir(ctx, expr.rhs)

    if expr_type is LtnNode:
        return gen_ltn_ir(ctx, lhs, rhs)

    elif expr_type is LeqNode:
        return gen_leq_ir(ctx, lhs, rhs)

    elif expr_type is GtnNode:
        return gen_gtn_ir(ctx, lhs, rhs)

    elif expr_type is GeqNode:
        return gen_geq_ir(ctx, lhs, rhs)

    elif expr_type is EqlNode:
        return gen_eql_ir(ctx, lhs, rhs)

    elif expr_type is NeqNode:
        return gen_neq_ir(ctx, lhs, rhs)

    elif expr_type is AssignExprNode:
        gen_assign_code(ctx, lhs, rhs)
        return lhs

    else:
        raise Todo(expr)

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

    elif val_type is AutoPtrType and as_type is PtrType:
        if type(value) is NilValue:
            return NilValue(ir_as_type)

        else:
            raise Todo()

    else:
        raise Todo(value)

def gen_init_ir(ctx, expr):
    rhs = gen_expr_ir(ctx, expr.rhs)
    lhs = StackValue(ctx, get_concrete_type(rhs.type))

    if type(expr.lhs) is SymbolNode:
        ctx.scope.resolve(expr.lhs.id).set_ir_value(lhs)

        gen_assign_code(ctx, lhs, rhs)

        return lhs

    else:
        raise Todo(expr)

def gen_assign_code(ctx, lhs, rhs):
    ctx.builder.store(
        gen_implicit_cast_ir(ctx, rhs, lhs.type).get_llvm_value(),
        lhs.get_llvm_ptr()
    )

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

def gen_and_ir(ctx, expr):
    and_lhs_true = ctx.builder.append_basic_block("and_lhs_true")
    and_true = ctx.builder.append_basic_block("and_true")
    and_false = ctx.builder.append_basic_block("and_false")
    and_end = ctx.builder.append_basic_block("and_end")

    ctx.builder.cbranch(
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.lhs)).get_llvm_value(),
        and_lhs_true,
        and_false
    )

    ctx.builder.position_at_start(and_end)
    phi = ctx.builder.phi(BitType().get_llvm_value())

    with ctx.builder.goto_block(and_lhs_true):
        ctx.builder.cbranch(
            gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.rhs)).get_llvm_value(),
            and_true,
            and_false
        )

    with ctx.builder.goto_block(and_true):
        phi.add_incoming(
            ir.IntType(1)(1),
            and_true
        )
        ctx.builder.branch(and_end)

    with ctx.builder.goto_block(and_false):
        phi.add_incoming(
            ir.IntType(1)(0),
            and_false
        )
        ctx.builder.branch(and_end)

    return LlvmValue(BitType(), phi)

def gen_or_ir(ctx, expr):
    or_lhs_false = ctx.builder.append_basic_block("or_lhs_false")
    or_true = ctx.builder.append_basic_block("or_true")
    or_false = ctx.builder.append_basic_block("or_false")
    or_end = ctx.builder.append_basic_block("or_end")

    ctx.builder.cbranch(
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.lhs)).get_llvm_value(),
        or_true,
        or_lhs_false
    )

    ctx.builder.position_at_start(or_end)
    phi = ctx.builder.phi(BitType().get_llvm_value())

    with ctx.builder.goto_block(or_lhs_false):
        ctx.builder.cbranch(
            gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.rhs)).get_llvm_value(),
            or_true,
            or_false
        )

    with ctx.builder.goto_block(or_true):
        phi.add_incoming(
            ir.IntType(1)(1),
            or_true
        )
        ctx.builder.branch(or_end)

    with ctx.builder.goto_block(or_false):
        phi.add_incoming(
            ir.IntType(1)(0),
            or_false
        )
        ctx.builder.branch(or_end)

    return LlvmValue(BitType(), phi)

def gen_not_ir(ctx, expr):
    return gen_bit_not_ir(
        ctx,
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.operand))
    )

def gen_xor_ir(ctx, expr):
    return gen_bit_xor_ir(
        ctx,
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.lhs)),
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.rhs))
    )

def _gen_fun_cmp(ctx, op, lhs, rhs):
    cmp_type = get_common_type(lhs.type, rhs.type)

    if type(cmp_type) is IntType:
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
    elif type(cmp_type) is PtrType:
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


def gen_bit_and_ir(ctx, lhs, rhs):
    raise Todo()

def gen_bit_or_ir(ctx, lhs, rhs):
    raise Todo()

def gen_bit_not_ir(ctx, operand):
    common_type = get_concrete_type(operand.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.not_(
                gen_implicit_cast_ir(
                    ctx, operand, common_type
                ).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_bit_xor_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.xor(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()
