from llvmlite import ir

from ..types import *

def gen_string_ir(ctx, expr):
    initializer = [ ]

    for c in expr.value:
        initializer.append(ir.IntType(8)(ord(c)))

    initializer.append(ir.IntType(8)(0))

    ir_type = ArrayType(
        IntValue(AutoIntType(), len(initializer)), IntType(8, False)
    )
    value = ir.GlobalVariable(
        ctx.builder.module,
        ir_type.get_llvm_value(),
        ".str{}".format(ctx.const_string_counter)
    )

    value.linkage = "private"
    value.global_constant = True
    value.initializer = ir.Constant.literal_array(initializer)

    ctx.const_string_counter += 1

    return LlvmRef(
        ctx,
        ir_type,
        value
    )


def gen_cglobal_ir(ctx, expr):
    from .exprs import gen_expr_ir
    
    ir_type = gen_expr_ir(ctx, expr.type)

    llvm_value = ir.GlobalVariable(
        ctx.builder.module, ir_type.get_llvm_value(), expr.id
    )
    llvm_value.global_constant = True

    value = LlvmRef(ctx, ir_type, llvm_value)

    ctx.scope.resolve(expr.id).set_ir_value(value)

    return value
