
from ...ast import *

from ..types import *

def gen_static_expr_ir(scope, expr):
    expr_type = type(expr)

    if expr_type is IntTypeNode:
        return IntType(expr.num_bits, expr.is_signed)

    elif expr_type is VoidTypeNode:
        return VoidType()

    elif expr_type is AutoIntNode:
        return IntValue(AutoIntType(), int(str(expr.value), expr.radix))

    elif expr_type is IntNode:
        return IntValue(
            IntType(expr.num_bits, expr.is_signed),
            int(str(expr.value), expr.radix)
        )

    elif expr_type is NilNode:
        return NilValue(AutoPtrType())

    elif expr_type is SymbolNode:
        return scope.resolve(expr.id).get_ir_value()

    elif expr_type is ArrayTypeNode:
        return gen_static_array_type_ir(scope, expr.length, expr.type)

    elif expr_type is EmbedCallExprNode:
        return gen_static_embed_call_ir(scope, expr)

    elif issubclass(expr_type, UnaryExprNode):
        return gen_static_unary_expr_ir(scope, expr)

    else:
        raise Todo(expr)


def gen_static_unary_expr_ir(scope, expr):
    expr_type = type(expr)
    operand = gen_static_expr_ir(scope, expr.operand)

    if expr_type is PtrExprNode:
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
