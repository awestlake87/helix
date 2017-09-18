from ..types import *

from .cast_exprs import gen_implicit_cast_ir
from .static_exprs import gen_static_ptr_expr_ir

def gen_ptr_ir(ctx, value):
    if issubclass(type(value), IrValue):
        if type(value.type) is PtrType:
            return LlvmRef(
                ctx,
                value.type.pointee,
                value.get_llvm_value()
            )
        else:
            raise Todo(value)

    else:
        return gen_static_ptr_expr_ir(ctx.scope, value)

def gen_ref_ir(ctx, value):
    if issubclass(type(value), LlvmRef):
        return LlvmValue(PtrType(value.type), value.get_llvm_ptr())

    else:
        raise Todo(value_type)

def gen_index_expr_ir(ctx, lhs, rhs):
    if type(lhs.type) is ArrayType:
        if issubclass(type(lhs), LlvmRef):
            return LlvmRef(
                ctx,
                lhs.type.elem_type,
                ctx.builder.gep(
                    lhs.get_llvm_ptr(),
                    [
                        ir.IntType(32)(0),
                        gen_implicit_cast_ir(
                            ctx, rhs, lhs.type.elem_type
                        ).get_llvm_value()
                    ]
                ),
                is_mut = lhs.is_mut
            )

        else:
            raise Todo()
    else:
        raise Todo()

def gen_ptr_add_ir(ctx, ptr, index):
    return LlvmValue(
        ptr.type,
        ctx.builder.gep(
            ptr.get_llvm_value(),
            [
                gen_implicit_cast_ir(
                    ctx, index, IntType(32, True)
                ).get_llvm_value()
            ]
        )
    )
