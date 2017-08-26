from llvmlite import ir

from ..types import *
from ...ast import *

def get_rtti_info(ctx, t):
    def get_extern_rtti_var(name):
        try:
            return ctx.builder.module.get_global(name)

        except KeyError as e:
            type_info = ir.GlobalVariable(
                ctx.builder.module, ir.IntType(8).as_pointer(), name
            )

            return type_info

    if type(t) is IntType:
        if t.num_bits == 32:
            if t.is_signed:
                return get_extern_rtti_var("_ZTIi")
            else:
                return get_extern_rtti_var("_ZTIj")

        elif t.num_bits == 8:
            if t.is_signed:
                return get_extern_rtti_var("_ZTIa")
            else:
                return get_extern_rtti_var("_ZTIh")

        else:
            raise Todo(t)
    else:
        raise Todo(t)

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
