from ..types import *

from ...ast import *

def gen_sizeof_ir(ctx, value):
    operand = None
    if issubclass(type(value), Type):
        operand = value
    else:
        operand = value.type


    nil_value = NilValue(PtrType(operand))
    size_type = IntType(32, False)

    return LlvmValue(
        size_type,
        ctx.builder.ptrtoint(
            ctx.builder.gep(
                nil_value.get_llvm_value(),
                [ ir.IntType(32)(1) ]
            ),
            size_type.get_llvm_value()
        )
    )

def gen_offsetof_ir(ctx, expr):
    from .exprs import gen_expr_ir

    lhs = gen_expr_ir(ctx, expr.lhs)

    if type(lhs) is StructType:
        if type(expr.rhs) is AttrNode:
            _, attr_index = lhs.get_attr_info(expr.rhs.id)
            nil_value = NilValue(PtrType(lhs))
            size_type = IntType(32, False)

            return LlvmValue(
                size_type,
                ctx.builder.ptrtoint(
                    ctx.builder.gep(
                        nil_value.get_llvm_value(),
                        [ ir.IntType(32)(0), ir.IntType(32)(attr_index) ]
                    ),
                    size_type.get_llvm_value()
                )
            )

    else:
        raise Todo(lhs)
