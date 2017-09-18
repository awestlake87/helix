from ..types import *

from .cast_exprs import gen_implicit_cast_ir, get_concrete_type

from ...ast import *
from ...err import Todo, ValueIsNotMut

def gen_init_ir(ctx, expr):
    from .exprs import gen_expr_ir

    lhs_node = expr.lhs
    lhs_type = type(lhs_node)

    is_mut = False

    if lhs_type is MutNode:
        is_mut = True

        lhs_node = lhs_node.operand
        lhs_type = type(lhs_node)

    rhs = gen_expr_ir(ctx, expr.rhs)

    if lhs_type is SymbolNode:
        lhs = StackValue(ctx, get_concrete_type(rhs.type), is_mut = is_mut)

        ctx.scope.resolve(lhs_node.id).ir_value = lhs

        gen_assign_code(ctx, lhs, rhs, is_init = True)

        return lhs

    elif lhs_type is GlobalNode:
        lhs = gen_expr_ir(ctx, lhs_node)

        gen_assign_code(ctx, lhs, rhs, is_init = True)

        return lhs

    else:
        raise Todo(expr)

def gen_assign_code(ctx, lhs, rhs, is_init = False):
    if lhs.is_mut or is_init:
        ctx.builder.store(
            gen_implicit_cast_ir(ctx, rhs, lhs.type).get_llvm_value(),
            lhs.get_llvm_ptr()
        )

    else:
        raise ValueIsNotMut()
