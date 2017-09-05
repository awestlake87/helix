

from ...ast import *
from ...err import Todo

from ..types import *
from ..values import *

from .access_exprs import *
from .assign_exprs import *
from .bitwise_exprs import *
from .call_exprs import *
from .cast_exprs import *
from .cmp_exprs import *
from .global_exprs import *
from .info_exprs import *
from .math_exprs import *
from .misc_exprs import *
from .ptr_exprs import *
from .static_exprs import *

def gen_expr_ir(ctx, expr):
    expr_type = type(expr)

    if expr_type is CallExprNode:
        return gen_call_ir(ctx, expr)

    elif expr_type is SymbolNode:
        value = ctx.scope.resolve(expr.id).get_ir_value()
        if type(value) is GlobalValue:
            return LlvmRef(ctx, value.type, value.get_llvm_ptr())
        else:
            return value

    elif expr_type is AttrNode:
        return gen_access_ir(ctx, ctx.instance, expr.id)

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

    elif expr_type is DotExprNode:
        return gen_dot_ir(ctx, expr)

    elif expr_type is OffsetofNode:
        return gen_offsetof_ir(ctx, expr)

    elif expr_type is TernaryConditionalNode:
        return gen_ternary_conditional_ir(ctx, expr)

    elif expr_type is GlobalNode:
        value = ctx.scope.resolve(expr.id).get_ir_value()
        return LlvmRef(
            ctx, value.type, value.get_llvm_ptr()
        )

    elif issubclass(expr_type, BinaryExprNode):
        return gen_binary_expr_ir(ctx, expr)

    elif issubclass(expr_type, UnaryExprNode):
        return gen_unary_expr_ir(ctx, expr)

    elif expr_type is StringNode:
        return gen_string_ir(ctx, expr)

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

    elif expr_type is AddExprNode:
        return gen_add_ir(ctx, lhs, rhs)
    elif expr_type is SubExprNode:
        return gen_sub_ir(ctx, lhs, rhs)
    elif expr_type is MulExprNode:
        return gen_mul_ir(ctx, lhs, rhs)
    elif expr_type is DivExprNode:
        return gen_div_ir(ctx, lhs, rhs)
    elif expr_type is ModExprNode:
        return gen_mod_ir(ctx, lhs, rhs)

    elif expr_type is BitAndExprNode:
        return gen_bit_and_ir(ctx, lhs, rhs)
    elif expr_type is BitOrExprNode:
        return gen_bit_or_ir(ctx, lhs, rhs)
    elif expr_type is BitXorExprNode:
        return gen_bit_xor_ir(ctx, lhs, rhs)
    elif expr_type is BitShlExprNode:
        return gen_bit_shl_ir(ctx, lhs, rhs)
    elif expr_type is BitShrExprNode:
        return gen_bit_shr_ir(ctx, lhs, rhs)

    elif expr_type is AssignExprNode:
        gen_assign_code(ctx, lhs, rhs)
        return lhs

    elif expr_type is AddAssignExprNode:
        gen_assign_code(ctx, lhs, gen_add_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is SubAssignExprNode:
        gen_assign_code(ctx, lhs, gen_sub_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is MulAssignExprNode:
        gen_assign_code(ctx, lhs, gen_mul_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is DivAssignExprNode:
        gen_assign_code(ctx, lhs, gen_div_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is ModAssignExprNode:
        gen_assign_code(ctx, lhs, gen_mod_ir(ctx, lhs, rhs))
        return lhs

    elif expr_type is BitAndAssignExprNode:
        gen_assign_code(ctx, lhs, gen_bit_and_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitOrAssignExprNode:
        gen_assign_code(ctx, lhs, gen_bit_or_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitXorAssignExprNode:
        gen_assign_code(ctx, lhs, gen_bit_xor_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitShlAssignExprNode:
        gen_assign_code(ctx, lhs, gen_bit_shl_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitShrAssignExprNode:
        gen_assign_code(ctx, lhs, gen_bit_shr_ir(ctx, lhs, rhs))
        return lhs

    elif expr_type is IndexExprNode:
        return gen_index_expr_ir(ctx, lhs, rhs)

    elif expr_type is AsNode:
        return gen_implicit_cast_ir(ctx, lhs, rhs)

    elif expr_type is CastNode:
        return gen_cast_ir(ctx, lhs, rhs)

    else:
        return gen_static_expr_ir(ctx.scope, expr)

def gen_unary_expr_ir(ctx, expr):
    operand = gen_expr_ir(ctx, expr.operand)

    expr_type = type(expr)

    if expr_type is PtrExprNode:
        return gen_ptr_expr_ir(ctx, operand)
    elif expr_type is RefExprNode:
        return gen_ref_expr_ir(ctx, operand)

    elif expr_type is PreIncExprNode:
        return gen_pre_inc_ir(ctx, operand)
    elif expr_type is PostIncExprNode:
        return gen_post_inc_ir(ctx, operand)
    elif expr_type is PreDecExprNode:
        return gen_pre_dec_ir(ctx, operand)
    elif expr_type is PostDecExprNode:
        return gen_post_dec_ir(ctx, operand)

    elif expr_type is NegExprNode:
        return gen_neg_ir(ctx, operand)

    elif expr_type is BitNotExprNode:
        return gen_bit_not_ir(ctx, operand)

    elif expr_type is SizeofNode:
        return gen_sizeof_ir(ctx, operand)

    else:
        raise Todo(expr)
