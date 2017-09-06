from ..types import *

def get_common_type(a, b):
    if a is b or a == b:
        return a

    elif type(a) is IntType and type(b) is AutoIntType:
        return a

    elif type(a) is AutoIntType and type(b) is IntType:
        return b

    elif type(a) is PtrType and type(b) is AutoPtrType:
        return a

    elif type(a) is AutoPtrType and type(b) is PtrType:
        return b

    else:
        raise Todo()

def get_concrete_type(t):
    if type(t) is AutoIntType:
        return IntType()
    else:
        return t

def gen_as_bit_ir(ctx, value):
    from .cmp_exprs import gen_neq_ir

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

    if val_type is ArrayType and as_type is PtrType:
        if value.type.elem_type == ir_as_type.pointee:
            if issubclass(type(value), LlvmRef):
                return LlvmValue(
                    PtrType(value.type.elem_type),
                    ctx.builder.gep(
                        value.get_llvm_ptr(),
                        [ ir.IntType(32)(0), ir.IntType(32)(0) ]
                    )
                )
            elif issubclass(type(value), LlvmValue):
                return LlvmValue(
                    PtrType(value.type.elem_type),
                    ctx.builder.gep(
                        value.get_llvm_value(),
                        [ ir.IntType(32)(0) ]
                    )
                )
            else:
                print(value)
                raise Todo()

        else:
            raise Todo("as is unsupported for this type")

    else:
        return gen_static_as_ir(ctx.scope, value, ir_as_type)

def gen_static_as_ir(scope, value, ir_as_type):
    val_type = type(value.type)
    as_type = type(ir_as_type)

    if value.type is ir_as_type or value.type == ir_as_type:
        return value

    elif val_type is AutoIntType and as_type is IntType:
        return IntValue(ir_as_type, value.value)

    elif val_type is AutoPtrType and as_type is PtrType:
        if type(value) is NilValue:
            return NilValue(ir_as_type)

        else:
            raise Todo()

    else:
        raise Todo(ir_as_type)


def gen_cast_ir(ctx, value, ir_as_type):
    val_type = type(value.type)
    as_type = type(ir_as_type)

    if value.type is ir_as_type or value.type == ir_as_type:
        return value

    elif val_type is PtrType and as_type is PtrType:
        return LlvmValue(
            ir_as_type,
            ctx.builder.bitcast(
                value.get_llvm_value(),
                ir_as_type.get_llvm_value()
            )
        )

    elif val_type is IntType and as_type is IntType:
        if value.type.num_bits < ir_as_type.num_bits:
            if not value.type.is_signed and not value.type.is_signed:
                return LlvmValue(
                    ir_as_type,
                    ctx.builder.zext(
                        value.get_llvm_value(),
                        ir_as_type.get_llvm_value()
                    )
                )
            else:
                raise Todo()

        else:
            raise Todo()


    else:
        raise Todo()
