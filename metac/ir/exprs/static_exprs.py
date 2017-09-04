
from ...info import *

from ..types import *

def gen_static_expr_ir(scope, expr_info):
    expr_type = type(expr_info)

    if expr_type is IntTypeInfo:
        return IntType(expr_info.num_bits, expr_info.is_signed)

    elif expr_type is VoidTypeInfo:
        return VoidType()

    elif expr_type is AutoTypeInfo:
        return AutoType()

    elif expr_type is AutoIntInfo:
        return IntValue(
            AutoIntType(), int(str(expr_info.value), expr_info.radix)
        )

    elif expr_type is IntInfo:
        return IntValue(
            IntType(expr_info.num_bits, expr_info.is_signed),
            int(str(expr_info.value), expr_info.radix)
        )

    elif expr_type is NilInfo:
        return NilValue(AutoPtrType())

    elif expr_type is SymbolInfo:
        return scope.resolve(expr_info.id).proto_target.ir_value

    elif expr_type is ArrayTypeInfo:
        return gen_static_array_type_ir(
            scope, expr_info.length, expr_info.type
        )

    elif expr_type is EmbedCallInfo:
        return gen_static_embed_call_ir(scope, expr_info)

    elif expr_type is CallInfo:
        return gen_static_call_ir(scope, expr_info)

    elif issubclass(expr_type, UnaryExprInfo):
        return gen_static_unary_expr_ir(scope, expr_info)

    else:
        raise Todo(expr_info)


def gen_static_unary_expr_ir(scope, expr):
    expr_type = type(expr)
    operand = gen_static_expr_ir(scope, expr.operand)

    if expr_type is PtrExprInfo:
        return gen_static_ptr_expr_ir(scope, operand)

    else:
        raise Todo(expr)

def gen_static_ptr_expr_ir(scope, operand):
    if issubclass(type(operand), Type):
        return PtrType(operand)

    else:
        raise Todo(operand)

def gen_static_array_type_ir(scope, length, elem_type):
    return ArrayType(
        gen_static_expr_ir(scope, length),
        gen_static_expr_ir(scope, elem_type)
    )

def gen_static_embed_call_ir(scope, expr):
    lhs = gen_static_expr_ir(scope, expr.lhs)

    if lhs == IntType(32, True):
        if len(expr.args) == 1:
            arg = gen_static_expr_ir(scope, expr.args[0])
            if type(arg) != IntValue:
                raise Todo("unexpected arg")
            else:
                return IntType(arg.value, True)

        else:
            raise Todo("embed int args")

    else:
        raise Todo(lhs)

def gen_static_call_ir(scope, expr):
    from .cast_exprs import gen_static_as_ir

    lhs = gen_static_expr_ir(scope, expr.lhs)

    value_type = type(lhs)

    if value_type is IntType:
        if len(expr.args) == 0:
            return LlvmValue(lhs, lhs.get_llvm_value()(ir.Undefined))

        elif len(expr.args) == 1:
            return gen_static_as_ir(
                scope, gen_static_expr_ir(ctx, expr.args[0]), lhs
            )

        else:
            raise Todo("int args")

    elif value_type is StructType:
        if len(expr.args) == 0:
            return LlvmValue(lhs, lhs.get_llvm_value()(ir.Undefined))

        else:
            raise Todo("struct args")

    elif value_type is PtrType:
        if len(expr.args) == 0:
            return LlvmValue(lhs, lhs.get_llvm_value()(ir.Undefined))

        elif len(expr.args) == 1:
            return gen_static_as_ir(
                ctx, gen_static_expr_ir(ctx, expr.args[0]), lhs
            )

        else:
            raise Todo("ptr args")

    elif value_type is ArrayType:
        if len(expr.args) == 0:
            return LlvmValue(lhs, lhs.get_llvm_value()(ir.Undefined))

        else:
            raise Todo("array args")

    else:
        raise Todo(lhs)
