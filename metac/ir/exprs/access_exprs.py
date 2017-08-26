from ..types import *

from ...ast import SymbolNode

def gen_dot_ir(ctx, expr):
    from .exprs import gen_expr_ir

    lhs = gen_expr_ir(ctx, expr.lhs)

    if type(lhs.type) is StructType:
        if type(expr.rhs) is SymbolNode:
            attr_type, attr_index = lhs.type.get_attr_info(expr.rhs.id)

            return LlvmRef(
                ctx,
                attr_type,
                ctx.builder.gep(
                    lhs.get_llvm_ptr(),
                    [ ir.IntType(32)(0), ir.IntType(32)(attr_index) ]
                )
            )

        else:
            raise Todo("rhs is not a symbol")

    else:
        raise Todo()
