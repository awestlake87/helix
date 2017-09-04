

from ...info import *
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

    if expr_type is CallExprInfo:
        return gen_call_ir(ctx, expr)

    elif expr_type is SymbolInfo:
        value = ctx.scope.resolve(expr.id).proto_target.ir_value
        if type(value) is GlobalValue:
            return LlvmRef(ctx, value.type, value.get_llvm_ptr())
        else:
            return value

    elif expr_type is AttrInfo:
        return gen_access_ir(ctx, ctx.instance, expr.id)

    elif expr_type is AndInfo:
        return gen_and_ir(ctx, expr)

    elif expr_type is OrInfo:
        return gen_or_ir(ctx, expr)

    elif expr_type is NotInfo:
        return gen_not_ir(ctx, expr)

    elif expr_type is XorInfo:
        return gen_xor_ir(ctx, expr)

    elif expr_type is InitExprInfo:
        return gen_init_ir(ctx, expr)

    elif expr_type is DotExprInfo:
        return gen_dot_ir(ctx, expr)

    elif expr_type is OffsetofInfo:
        return gen_offsetof_ir(ctx, expr)

    elif expr_type is TernaryConditionalInfo:
        return gen_ternary_conditional_ir(ctx, expr)

    elif expr_type is GlobalInfo:
        value = ctx.scope.resolve(expr.id).get_ir_value()
        return LlvmRef(
            ctx, value.type, value.get_llvm_ptr()
        )

    elif issubclass(expr_type, BinaryExprInfo):
        return gen_binary_expr_ir(ctx, expr)

    elif issubclass(expr_type, UnaryExprInfo):
        return gen_unary_expr_ir(ctx, expr)

    elif expr_type is StringInfo:
        return gen_string_ir(ctx, expr)

    else:
        return gen_static_expr_ir(ctx.scope, expr)

def gen_binary_expr_ir(ctx, expr):
    expr_type = type(expr)
    lhs = gen_expr_ir(ctx, expr.lhs)
    rhs = gen_expr_ir(ctx, expr.rhs)

    if expr_type is LtnInfo:
        return gen_ltn_ir(ctx, lhs, rhs)
    elif expr_type is LeqInfo:
        return gen_leq_ir(ctx, lhs, rhs)
    elif expr_type is GtnInfo:
        return gen_gtn_ir(ctx, lhs, rhs)
    elif expr_type is GeqInfo:
        return gen_geq_ir(ctx, lhs, rhs)
    elif expr_type is EqlInfo:
        return gen_eql_ir(ctx, lhs, rhs)
    elif expr_type is NeqInfo:
        return gen_neq_ir(ctx, lhs, rhs)

    elif expr_type is AddExprInfo:
        return gen_add_ir(ctx, lhs, rhs)
    elif expr_type is SubExprInfo:
        return gen_sub_ir(ctx, lhs, rhs)
    elif expr_type is MulExprInfo:
        return gen_mul_ir(ctx, lhs, rhs)
    elif expr_type is DivExprInfo:
        return gen_div_ir(ctx, lhs, rhs)
    elif expr_type is ModExprInfo:
        return gen_mod_ir(ctx, lhs, rhs)

    elif expr_type is BitAndExprInfo:
        return gen_bit_and_ir(ctx, lhs, rhs)
    elif expr_type is BitOrExprInfo:
        return gen_bit_or_ir(ctx, lhs, rhs)
    elif expr_type is BitXorExprInfo:
        return gen_bit_xor_ir(ctx, lhs, rhs)
    elif expr_type is BitShlExprInfo:
        return gen_bit_shl_ir(ctx, lhs, rhs)
    elif expr_type is BitShrExprInfo:
        return gen_bit_shr_ir(ctx, lhs, rhs)

    elif expr_type is AssignExprInfo:
        gen_assign_code(ctx, lhs, rhs)
        return lhs

    elif expr_type is AddAssignExprInfo:
        gen_assign_code(ctx, lhs, gen_add_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is SubAssignExprInfo:
        gen_assign_code(ctx, lhs, gen_sub_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is MulAssignExprInfo:
        gen_assign_code(ctx, lhs, gen_mul_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is DivAssignExprInfo:
        gen_assign_code(ctx, lhs, gen_div_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is ModAssignExprInfo:
        gen_assign_code(ctx, lhs, gen_mod_ir(ctx, lhs, rhs))
        return lhs

    elif expr_type is BitAndAssignExprInfo:
        gen_assign_code(ctx, lhs, gen_bit_and_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitOrAssignExprInfo:
        gen_assign_code(ctx, lhs, gen_bit_or_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitXorAssignExprInfo:
        gen_assign_code(ctx, lhs, gen_bit_xor_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitShlAssignExprInfo:
        gen_assign_code(ctx, lhs, gen_bit_shl_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitShrAssignExprInfo:
        gen_assign_code(ctx, lhs, gen_bit_shr_ir(ctx, lhs, rhs))
        return lhs

    elif expr_type is IndexExprInfo:
        return gen_index_expr_ir(ctx, lhs, rhs)

    elif expr_type is AsInfo:
        return gen_implicit_cast_ir(ctx, lhs, rhs)

    elif expr_type is CastInfo:
        return gen_cast_ir(ctx, lhs, rhs)

    else:
        return gen_static_expr_ir(ctx.scope, expr)

def gen_unary_expr_ir(ctx, expr):
    operand = gen_expr_ir(ctx, expr.operand)

    expr_type = type(expr)

    if expr_type is PtrExprInfo:
        return gen_ptr_expr_ir(ctx, operand)
    elif expr_type is RefExprInfo:
        return gen_ref_expr_ir(ctx, operand)

    elif expr_type is PreIncExprInfo:
        return gen_pre_inc_ir(ctx, operand)
    elif expr_type is PostIncExprInfo:
        return gen_post_inc_ir(ctx, operand)
    elif expr_type is PreDecExprInfo:
        return gen_pre_dec_ir(ctx, operand)
    elif expr_type is PostDecExprInfo:
        return gen_post_dec_ir(ctx, operand)

    elif expr_type is NegExprInfo:
        return gen_neg_ir(ctx, operand)

    elif expr_type is BitNotExprInfo:
        return gen_bit_not_ir(ctx, operand)

    elif expr_type is SizeofInfo:
        return gen_sizeof_ir(ctx, operand)

    else:
        raise Todo(expr)
