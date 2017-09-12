from ..types import *

def gen_dot_ir(ctx, expr):
    from ...sym import DataAttrSym, AttrFunSym, SymbolSym
    from .exprs import gen_expr_ir

    lhs = gen_expr_ir(ctx, expr.lhs)

    if type(expr.rhs) is SymbolSym:
        return gen_access_ir(ctx, lhs, expr.rhs.id)

    else:
        raise Todo(expr.rhs)

def gen_access_ir(ctx, lhs, rhs):
    from ...sym import DataAttrSym, AttrFunSym

    if type(lhs.type) is StructType:
        if type(rhs) is str:
            symbol = lhs.type.get_attr_symbol(rhs)

            if type(symbol) is DataAttrSym:
                return LlvmRef(
                    ctx,
                    symbol.ir_type,
                    ctx.builder.gep(
                        lhs.get_llvm_ptr(),
                        [ ir.IntType(32)(0), ir.IntType(32)(symbol.index) ]
                    )
                )

            elif type(symbol) is AttrFunSym:
                if issubclass(type(lhs), LlvmRef):
                    return BoundAttrFunValue(lhs, symbol.ir_value)
                else:
                    raise Todo("rval instance args?")

            else:
                raise Todo(symbol)

        else:
            raise Todo("rhs is not a symbol")

    else:
        raise Todo()
