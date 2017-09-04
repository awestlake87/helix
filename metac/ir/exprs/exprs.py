

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

    if expr_type is CallInfo:
        return gen_call_ir(ctx, expr)

    elif expr_type is SymbolInfo:
        value = ctx.scope.resolve(expr.id).ir_value
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

    elif expr_type is InitInfo:
        return gen_init_ir(ctx, expr)

    elif expr_type is DotInfo:
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

    elif issubclass(expr_type, BinaryInfo):
        return gen_binary_expr_ir(ctx, expr)

    elif issubclass(expr_type, UnaryInfo):
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

    elif expr_type is AddInfo:
        return gen_add_ir(ctx, lhs, rhs)
    elif expr_type is SubInfo:
        return gen_sub_ir(ctx, lhs, rhs)
    elif expr_type is MulInfo:
        return gen_mul_ir(ctx, lhs, rhs)
    elif expr_type is DivInfo:
        return gen_div_ir(ctx, lhs, rhs)
    elif expr_type is ModInfo:
        return gen_mod_ir(ctx, lhs, rhs)

    elif expr_type is BitAndInfo:
        return gen_bit_and_ir(ctx, lhs, rhs)
    elif expr_type is BitOrInfo:
        return gen_bit_or_ir(ctx, lhs, rhs)
    elif expr_type is BitXorInfo:
        return gen_bit_xor_ir(ctx, lhs, rhs)
    elif expr_type is BitShlInfo:
        return gen_bit_shl_ir(ctx, lhs, rhs)
    elif expr_type is BitShrInfo:
        return gen_bit_shr_ir(ctx, lhs, rhs)

    elif expr_type is AssignInfo:
        gen_assign_code(ctx, lhs, rhs)
        return lhs

    elif expr_type is AddAssignInfo:
        gen_assign_code(ctx, lhs, gen_add_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is SubAssignInfo:
        gen_assign_code(ctx, lhs, gen_sub_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is MulAssignInfo:
        gen_assign_code(ctx, lhs, gen_mul_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is DivAssignInfo:
        gen_assign_code(ctx, lhs, gen_div_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is ModAssignInfo:
        gen_assign_code(ctx, lhs, gen_mod_ir(ctx, lhs, rhs))
        return lhs

    elif expr_type is BitAndAssignInfo:
        gen_assign_code(ctx, lhs, gen_bit_and_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitOrAssignInfo:
        gen_assign_code(ctx, lhs, gen_bit_or_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitXorAssignInfo:
        gen_assign_code(ctx, lhs, gen_bit_xor_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitShlAssignInfo:
        gen_assign_code(ctx, lhs, gen_bit_shl_ir(ctx, lhs, rhs))
        return lhs
    elif expr_type is BitShrAssignInfo:
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

    elif expr_type is PreIncInfo:
        return gen_pre_inc_ir(ctx, operand)
    elif expr_type is PostIncInfo:
        return gen_post_inc_ir(ctx, operand)
    elif expr_type is PreDecInfo:
        return gen_pre_dec_ir(ctx, operand)
    elif expr_type is PostDecInfo:
        return gen_post_dec_ir(ctx, operand)

    elif expr_type is NegInfo:
        return gen_neg_ir(ctx, operand)

    elif expr_type is BitNotInfo:
        return gen_bit_not_ir(ctx, operand)

    elif expr_type is SizeofInfo:
        return gen_sizeof_ir(ctx, operand)

    else:
        raise Todo(expr)
