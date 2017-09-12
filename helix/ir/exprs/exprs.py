
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
    from ...sym import (
        CallSym,
        SymbolSym,
        AttrSym,
        AndSym,
        OrSym,
        NotSym,
        XorSym,
        InitSym,
        DotSym,
        OffsetofSym,
        TernaryConditionalSym,
        GlobalSym,
        BinaryExprSym,
        UnaryExprSym,
        StringSym
    )

    expr_type = type(expr)

    if expr_type is CallSym:
        return gen_call_ir(ctx, expr)

    elif expr_type is SymbolSym:
        value = ctx.scope.resolve(expr.id).ir_value
        if type(value) is GlobalValue:
            return LlvmRef(ctx, value.type, value.get_llvm_ptr())
        else:
            return value

    elif expr_type is AttrSym:
        return gen_access_ir(ctx, ctx.instance, expr.id)

    elif expr_type is AndSym:
        return gen_and_ir(ctx, expr)

    elif expr_type is OrSym:
        return gen_or_ir(ctx, expr)

    elif expr_type is NotSym:
        return gen_not_ir(ctx, expr)

    elif expr_type is XorSym:
        return gen_xor_ir(ctx, expr)

    elif expr_type is InitSym:
        return gen_init_ir(ctx, expr)

    elif expr_type is DotSym:
        return gen_dot_ir(ctx, expr)

    elif expr_type is OffsetofSym:
        return gen_offsetof_ir(ctx, expr)

    elif expr_type is TernaryConditionalSym:
        return gen_ternary_conditional_ir(ctx, expr)

    elif expr_type is GlobalSym:
        value = ctx.scope.resolve(expr.id).ir_value
        return LlvmRef(
            ctx, value.type, value.get_llvm_ptr()
        )

    elif issubclass(expr_type, BinaryExprSym):
        return gen_binary_expr_ir(ctx, expr)

    elif issubclass(expr_type, UnaryExprSym):
        return gen_unary_expr_ir(ctx, expr)

    elif expr_type is StringSym:
        return gen_string_ir(ctx, expr)

    else:
        return gen_static_expr_ir(ctx.scope, expr)

def gen_binary_expr_ir(ctx, expr):
    expr_type = type(expr)
    lhs = gen_expr_ir(ctx, expr.lhs)
    rhs = gen_expr_ir(ctx, expr.rhs)

    if expr_type is LtnSym:
        return gen_ltn_ir(ctx, lhs, rhs)
    elif expr_type is LeqSym:
        return gen_leq_ir(ctx, lhs, rhs)
    elif expr_type is GtnSym:
        return gen_gtn_ir(ctx, lhs, rhs)
    elif expr_type is GeqSym:
        return gen_geq_ir(ctx, lhs, rhs)
    elif expr_type is EqlSym:
        return gen_eql_ir(ctx, lhs, rhs)
    elif expr_type is NeqSym:
        return gen_neq_ir(ctx, lhs, rhs)

    elif expr_type is AddSym:
        return gen_add_ir(ctx, lhs, rhs)
    elif expr_type is SubSym:
        return gen_sub_ir(ctx, lhs, rhs)
    elif expr_type is MulSym:
        return gen_mul_ir(ctx, lhs, rhs)
    elif expr_type is DivSym:
        return gen_div_ir(ctx, lhs, rhs)
    elif expr_type is ModSym:
        return gen_mod_ir(ctx, lhs, rhs)

    elif expr_type is BitAndSym:
        return gen_bit_and_ir(ctx, lhs, rhs)
    elif expr_type is BitOrSym:
        return gen_bit_or_ir(ctx, lhs, rhs)
    elif expr_type is BitXorSym:
        return gen_bit_xor_ir(ctx, lhs, rhs)
    elif expr_type is BitShlSym:
        return gen_bit_shl_ir(ctx, lhs, rhs)
    elif expr_type is BitShrSym:
        return gen_bit_shr_ir(ctx, lhs, rhs)

    elif expr_type is AssignSym:
        gen_assign_code(ctx, lhs, rhs)
        return lhs

    elif expr_type is IndexSym:
        return gen_index_expr_ir(ctx, lhs, rhs)

    elif expr_type is AsSym:
        return gen_implicit_cast_ir(ctx, lhs, rhs)

    elif expr_type is CastSym:
        return gen_cast_ir(ctx, lhs, rhs)

    else:
        return gen_static_expr_ir(ctx.scope, expr)

def gen_unary_expr_ir(ctx, expr):
    operand = gen_expr_ir(ctx, expr.operand)

    expr_type = type(expr)

    if expr_type is PtrSym:
        return gen_ptr_expr_ir(ctx, operand)
    elif expr_type is RefSym:
        return gen_ref_expr_ir(ctx, operand)

    elif expr_type is PreIncSym:
        return gen_pre_inc_ir(ctx, operand)
    elif expr_type is PostIncSym:
        return gen_post_inc_ir(ctx, operand)
    elif expr_type is PreDecSym:
        return gen_pre_dec_ir(ctx, operand)
    elif expr_type is PostDecSym:
        return gen_post_dec_ir(ctx, operand)

    elif expr_type is NegSym:
        return gen_neg_ir(ctx, operand)

    elif expr_type is BitNotSym:
        return gen_bit_not_ir(ctx, operand)

    elif expr_type is SizeofSym:
        return gen_sizeof_ir(ctx, operand)

    else:
        raise Todo(expr)
