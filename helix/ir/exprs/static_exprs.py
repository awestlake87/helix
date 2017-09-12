
from ...sym import *

from ..types import *

def gen_static_expr_ir(scope, expr):
    expr_type = type(expr)

    if expr_type is IntTypeSym:
        return IntType(expr.num_bits, expr.is_signed)

    elif expr_type is VoidTypeSym:
        return VoidType()

    elif expr_type is AutoTypeSym:
        return AutoType()

    elif expr_type is AutoIntSym:
        return IntValue(AutoIntType(), int(str(expr.value), expr.radix))

    elif expr_type is IntSym:
        return IntValue(
            IntType(expr.num_bits, expr.is_signed),
            int(str(expr.value), expr.radix)
        )

    elif expr_type is NilSym:
        return NilValue(AutoPtrType())

    elif expr_type is SymbolSym:
        return scope.resolve(expr.id).ir_value

    elif expr_type is ArrayTypeSym:
        return gen_static_array_type_ir(scope, expr.length, expr.type)

    elif expr_type is EmbedCallSym:
        return gen_static_embed_call_ir(scope, expr)

    elif expr_type is CallSym:
        return gen_static_call_ir(scope, expr)

    elif issubclass(expr_type, UnaryExprSym):
        return gen_static_unary_expr_ir(scope, expr)

    else:
        raise Todo(expr)


def gen_static_unary_expr_ir(scope, expr):
    expr_type = type(expr)
    operand = gen_static_expr_ir(scope, expr.operand)

    if expr_type is PtrSym:
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
