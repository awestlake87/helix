

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

def gen_implicit_cast_ir(ctx, value, ir_as_type):
    val_type = type(value.type)
    as_type = type(ir_as_type)

    if val_type is as_type or val_type == as_type:
        return value

    elif val_type is AutoIntType and as_type is IntType:
        return IntValue(ir_as_type, value.value)

    else:
        raise Todo(value)

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
