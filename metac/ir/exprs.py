

from ..ast import *
from ..err import Todo

from .types import *
from .values import *

def gen_static_expr_ir(scope, expr):
    expr_type = type(expr)

    if expr_type is IntTypeNode:
        return IntType(expr.num_bits, expr.is_signed)

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

def gen_string_ir(ctx, expr):
    initializer = [ ]

    for c in expr.value:
        initializer.append(ir.IntType(8)(ord(c)))

    initializer.append(ir.IntType(8)(0))

    ir_type = ArrayType(
        IntValue(AutoIntType(), len(initializer)), IntType(8, False)
    )
    value = ir.GlobalVariable(
        ctx.builder.module,
        ir_type.get_llvm_value(),
        ".str{}".format(ctx.const_string_counter)
    )

    value.linkage = "private"
    value.global_constant = True
    value.initializer = ir.Constant.literal_array(initializer)

    ctx.const_string_counter += 1

    return LlvmRef(
        ctx,
        ir_type,
        value
    )

def gen_expr_ir(ctx, expr):
    expr_type = type(expr)

    if expr_type is CallExprNode:
        return gen_call_ir(ctx, expr)

    elif expr_type is SymbolNode:
        return ctx.scope.resolve(expr.id).get_ir_value()

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

    elif expr_type is TernaryConditionalNode:
        return gen_ternary_conditional_ir(ctx, expr)

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

    else:
        raise Todo(expr)

def gen_as_bit_ir(ctx, value):
    val_type = type(value.type)

    if value.type == BitType():
        return value

    elif val_type is IntType:
        return gen_neq_ir(ctx, value, IntValue(value.type, 0))

    else:
        raise Todo()

def gen_ptr_expr_ir(ctx, value):
    if issubclass(type(value), IrValue):
        if type(value.type) is PtrType:
            return LlvmValue(
                value.type.pointee, ctx.builder.load(value.get_llvm_value())
            )
        else:
            raise Todo(value)

    else:
        return gen_static_ptr_expr_ir(ctx.scope, value)

def gen_ref_expr_ir(ctx, value):
    if issubclass(type(value), LlvmRef):
        return LlvmValue(PtrType(value.type), value.get_llvm_ptr())

    else:
        raise Todo(value_type)

def gen_implicit_cast_ir(ctx, value, ir_as_type):
    val_type = type(value.type)
    as_type = type(ir_as_type)

    if value.type is ir_as_type or value.type == ir_as_type:
        return value

    elif val_type is AutoIntType and as_type is IntType:
        return IntValue(ir_as_type, value.value)

    elif val_type is AutoPtrType and as_type is PtrType:
        if type(value) is NilValue:
            return NilValue(ir_as_type)

        else:
            raise Todo()

    elif val_type is ArrayType and as_type is PtrType:
        if value.type.elem_type == ir_as_type.pointee:
            if issubclass(type(value), LlvmRef):
                return LlvmValue(
                    PtrType(value.type.elem_type),
                    ctx.builder.gep(
                        value.get_llvm_ptr(),
                        [ ir.IntType(32)(0), ir.IntType(32)(0) ]
                    )
                )
            elif issubclass(type(value), LlvmValue):
                return LlvmValue(
                    PtrType(value.type.elem_type),
                    ctx.builder.gep(
                        value.get_llvm_value(),
                        [ ir.IntType(32)(0) ]
                    )
                )
            else:
                print(value)
                raise Todo()

        else:
            raise Todo("as is unsupported for this type")

    else:
        raise Todo(value)

def gen_init_ir(ctx, expr):
    rhs = gen_expr_ir(ctx, expr.rhs)
    lhs = StackValue(ctx, get_concrete_type(rhs.type))

    if type(expr.lhs) is SymbolNode:
        ctx.scope.resolve(expr.lhs.id).set_ir_value(lhs)

        gen_assign_code(ctx, lhs, rhs)

        return lhs

    else:
        raise Todo(expr)

def gen_dot_ir(ctx, expr):
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

def gen_index_expr_ir(ctx, lhs, rhs):
    if type(lhs.type) is ArrayType:
        if issubclass(type(lhs), LlvmRef):
            return LlvmRef(
                ctx,
                lhs.type.elem_type,
                ctx.builder.gep(
                    lhs.get_llvm_ptr(),
                    [
                        ir.IntType(32)(0),
                        gen_implicit_cast_ir(
                            ctx, rhs, lhs.type.elem_type
                        ).get_llvm_value()
                    ]
                )
            )

        else:
            raise Todo()
    else:
        raise Todo()

def gen_ptr_add_ir(ctx, ptr, index):
    return LlvmValue(
        ptr.type,
        ctx.builder.gep(
            ptr.get_llvm_value(),
            [
                gen_implicit_cast_ir(
                    ctx, index, IntType(32, True)
                ).get_llvm_value()
            ]
        )
    )

def gen_ternary_conditional_ir(ctx, expr):
    tern_true = ctx.builder.append_basic_block("tern_true")
    tern_false = ctx.builder.append_basic_block("tern_false")
    tern_end = ctx.builder.append_basic_block("tern_end")

    ctx.builder.cbranch(
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.condition)).get_llvm_value(),
        tern_true,
        tern_false
    )

    lhs_value = None
    rhs_value = None

    with ctx.builder.goto_block(tern_true):
        lhs_value = gen_expr_ir(ctx, expr.lhs)
        ctx.builder.branch(tern_end)

    with ctx.builder.goto_block(tern_false):
        rhs_value = gen_expr_ir(ctx, expr.rhs)
        ctx.builder.branch(tern_end)

    val_type = get_concrete_type(
        get_common_type(lhs_value.type, rhs_value.type)
    )

    ctx.builder.position_at_start(tern_end)
    phi = ctx.builder.phi(val_type.get_llvm_value())

    phi.add_incoming(
        gen_implicit_cast_ir(ctx, lhs_value, val_type).get_llvm_value(),
        tern_true
    )
    phi.add_incoming(
        gen_implicit_cast_ir(ctx, rhs_value, val_type).get_llvm_value(),
        tern_false
    )

    return LlvmValue(val_type, phi)


def gen_assign_code(ctx, lhs, rhs):
    ctx.builder.store(
        gen_implicit_cast_ir(ctx, rhs, lhs.type).get_llvm_value(),
        lhs.get_llvm_ptr()
    )

def gen_call_ir(ctx, expr):
    lhs = gen_expr_ir(ctx, expr.lhs)

    value_type = type(lhs)

    if value_type is FunValue:
        ir_args = [ ]

        if lhs.type.is_vargs:
            if len(expr.args) >= len(lhs.type.param_types):
                num_params = len(lhs.type.param_types)

                for i in range(0, len(expr.args)):
                    if i < num_params:
                        ir_args.append(
                            gen_implicit_cast_ir(
                                ctx,
                                gen_expr_ir(ctx, expr.args[i]),
                                lhs.type.param_types[i]
                            ).get_llvm_value()
                        )
                    else:
                        arg_value = gen_expr_ir(ctx, expr.args[i])
                        concrete_type = get_concrete_type(arg_value.type)

                        ir_args.append(
                            gen_implicit_cast_ir(
                                ctx,
                                arg_value,
                                concrete_type
                            ).get_llvm_value()
                        )

            else:
                raise Todo("minimum args for vargs function")

        elif len(expr.args) == len(lhs.type.param_types):
            for arg_node, param_type in zip(expr.args, lhs.type.param_types):
                ir_args.append(
                    gen_implicit_cast_ir(
                        ctx, gen_expr_ir(ctx, arg_node), param_type
                    ).get_llvm_value()
                )
        else:
            raise Todo("arg length mismatch")

        return LlvmValue(
            lhs.type.ret_type, ctx.builder.call(lhs.get_llvm_value(), ir_args)
        )

    elif value_type is IntType:
        if len(expr.args) == 0:
            return LlvmValue(lhs, lhs.get_llvm_value()(ir.Undefined))

        elif len(expr.args) == 1:
            return gen_implicit_cast_ir(
                ctx, gen_expr_ir(ctx, expr.args[0]), lhs
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
            return gen_implicit_cast_ir(
                ctx, gen_expr_ir(ctx, expr.args[0]), lhs
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

def gen_and_ir(ctx, expr):
    and_lhs_true = ctx.builder.append_basic_block("and_lhs_true")
    and_true = ctx.builder.append_basic_block("and_true")
    and_false = ctx.builder.append_basic_block("and_false")
    and_end = ctx.builder.append_basic_block("and_end")

    ctx.builder.cbranch(
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.lhs)).get_llvm_value(),
        and_lhs_true,
        and_false
    )

    ctx.builder.position_at_start(and_end)
    phi = ctx.builder.phi(BitType().get_llvm_value())

    with ctx.builder.goto_block(and_lhs_true):
        ctx.builder.cbranch(
            gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.rhs)).get_llvm_value(),
            and_true,
            and_false
        )

    with ctx.builder.goto_block(and_true):
        phi.add_incoming(
            ir.IntType(1)(1),
            and_true
        )
        ctx.builder.branch(and_end)

    with ctx.builder.goto_block(and_false):
        phi.add_incoming(
            ir.IntType(1)(0),
            and_false
        )
        ctx.builder.branch(and_end)

    return LlvmValue(BitType(), phi)

def gen_or_ir(ctx, expr):
    or_lhs_false = ctx.builder.append_basic_block("or_lhs_false")
    or_true = ctx.builder.append_basic_block("or_true")
    or_false = ctx.builder.append_basic_block("or_false")
    or_end = ctx.builder.append_basic_block("or_end")

    ctx.builder.cbranch(
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.lhs)).get_llvm_value(),
        or_true,
        or_lhs_false
    )

    ctx.builder.position_at_start(or_end)
    phi = ctx.builder.phi(BitType().get_llvm_value())

    with ctx.builder.goto_block(or_lhs_false):
        ctx.builder.cbranch(
            gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.rhs)).get_llvm_value(),
            or_true,
            or_false
        )

    with ctx.builder.goto_block(or_true):
        phi.add_incoming(
            ir.IntType(1)(1),
            or_true
        )
        ctx.builder.branch(or_end)

    with ctx.builder.goto_block(or_false):
        phi.add_incoming(
            ir.IntType(1)(0),
            or_false
        )
        ctx.builder.branch(or_end)

    return LlvmValue(BitType(), phi)

def gen_not_ir(ctx, expr):
    return gen_bit_not_ir(
        ctx,
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.operand))
    )

def gen_xor_ir(ctx, expr):
    return gen_bit_xor_ir(
        ctx,
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.lhs)),
        gen_as_bit_ir(ctx, gen_expr_ir(ctx, expr.rhs))
    )

def _gen_fun_cmp(ctx, op, lhs, rhs):
    cmp_type = get_common_type(lhs.type, rhs.type)

    if type(cmp_type) is IntType:
        if cmp_type.is_signed:
            return LlvmValue(
                BitType(),
                ctx.builder.icmp_signed(
                    op,
                    gen_implicit_cast_ir(ctx, lhs, cmp_type).get_llvm_value(),
                    gen_implicit_cast_ir(ctx, rhs, cmp_type).get_llvm_value()
                )
            )
        else:
            return LlvmValue(
                BitType(),
                ctx.builder.icmp_unsigned(
                    op,
                    gen_implicit_cast_ir(ctx, lhs, cmp_type).get_llvm_value(),
                    gen_implicit_cast_ir(ctx, rhs, cmp_type).get_llvm_value()
                )
            )
    elif type(cmp_type) is PtrType:
        return LlvmValue(
            BitType(),
            ctx.builder.icmp_unsigned(
                op,
                gen_implicit_cast_ir(ctx, lhs, cmp_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, cmp_type).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_ltn_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "<", lhs, rhs)

def gen_leq_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "<=", lhs, rhs)

def gen_gtn_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, ">", lhs, rhs)

def gen_geq_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, ">=", lhs, rhs)

def gen_eql_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "==", lhs, rhs)

def gen_neq_ir(ctx, lhs, rhs):
    return _gen_fun_cmp(ctx, "!=", lhs, rhs)

def gen_neg_ir(ctx, operand):
    t = get_concrete_type(operand.type)

    if type(t) is IntType:
        return LlvmValue(
            t,
            ctx.builder.neg(
                gen_implicit_cast_ir(ctx, operand, t).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_add_ir(ctx, lhs, rhs):
    if (
        type(lhs.type) is PtrType and (
            type(rhs.type) is IntType or type(rhs.type) is AutoIntType
        )
    ):
        return gen_ptr_add_ir(ctx, lhs, rhs)

    elif (
        type(rhs.type) is PtrType and (
            type(lhs.type) is IntType or type(lhs.type) is AutoIntType
        )
    ):
        return gen_ptr_add_ir(ctx, rhs, lhs)

    else:
        common_type = get_concrete_type(get_common_type(lhs.type, rhs.type))

        if type(common_type) is IntType:
            return LlvmValue(
                common_type,
                ctx.builder.add(
                    gen_implicit_cast_ir(
                        ctx, lhs, common_type
                    ).get_llvm_value(),
                    gen_implicit_cast_ir(
                        ctx, rhs, common_type
                    ).get_llvm_value()
                )
            )

        else:
            raise Todo()

def gen_sub_ir(ctx, lhs, rhs):
    if (
        type(lhs.type) is PtrType and (
            type(rhs.type) is IntType or type(rhs.type) is AutoIntType
        )
    ):
        return gen_ptr_add_ir(ctx, lhs, gen_neg_ir(ctx, rhs))

    elif (
        type(rhs.type) is PtrType and (
            type(lhs.type) is IntType or type(lhs.type) is AutoIntType
        )
    ):
        return gen_ptr_add_ir(ctx, rhs, gen_neg_ir(ctx, lhs))

    else:
        common_type = get_concrete_type(get_common_type(lhs.type, rhs.type))

        if type(common_type) is IntType:
            return LlvmValue(
                common_type,
                ctx.builder.sub(
                    gen_implicit_cast_ir(
                        ctx, lhs, common_type
                    ).get_llvm_value(),
                    gen_implicit_cast_ir(
                        ctx, rhs, common_type
                    ).get_llvm_value()
                )
            )

        else:
            raise Todo()

def gen_mul_ir(ctx, lhs, rhs):
    common_type = get_concrete_type(get_common_type(lhs.type, rhs.type))

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.mul(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_div_ir(ctx, lhs, rhs):
    common_type = get_concrete_type(get_common_type(lhs.type, rhs.type))

    if type(common_type) is IntType:
        if common_type.is_signed:
            return LlvmValue(
                common_type,
                ctx.builder.sdiv(
                    gen_implicit_cast_ir(
                        ctx, lhs, common_type
                    ).get_llvm_value(),
                    gen_implicit_cast_ir(
                        ctx, rhs, common_type
                    ).get_llvm_value()
                )
            )
        else:
            return LlvmValue(
                common_type,
                ctx.builder.udiv(
                    gen_implicit_cast_ir(
                        ctx, lhs, common_type
                    ).get_llvm_value(),
                    gen_implicit_cast_ir(
                        ctx, rhs, common_type
                    ).get_llvm_value()
                )
            )

    else:
        raise Todo()

def gen_mod_ir(ctx, lhs, rhs):
    common_type = get_concrete_type(get_common_type(lhs.type, rhs.type))

    if type(common_type) is IntType:
        if common_type.is_signed:
            return LlvmValue(
                common_type,
                ctx.builder.srem(
                    gen_implicit_cast_ir(
                        ctx, lhs, common_type
                    ).get_llvm_value(),
                    gen_implicit_cast_ir(
                        ctx, rhs, common_type
                    ).get_llvm_value()
                )
            )
        else:
            return LlvmValue(
                common_type,
                ctx.builder.urem(
                    gen_implicit_cast_ir(
                        ctx, lhs, common_type
                    ).get_llvm_value(),
                    gen_implicit_cast_ir(
                        ctx, rhs, common_type
                    ).get_llvm_value()
                )
            )

    else:
        raise Todo()

def gen_pre_inc_ir(ctx, operand):
    if type(operand.type) is IntType:
        gen_assign_code(
            ctx,
            operand,
            gen_add_ir(ctx, operand, IntValue(operand.type, 1))
        )
        return operand

    else:
        raise Todo()

def gen_post_inc_ir(ctx, operand):
    if type(operand.type) is IntType:
        value = LlvmValue(operand.type, operand.get_llvm_value())

        gen_assign_code(
            ctx,
            operand,
            gen_add_ir(ctx, operand, IntValue(operand.type, 1))
        )

        return value

    else:
        raise Todo()

def gen_pre_dec_ir(ctx, operand):
    if type(operand.type) is IntType:
        gen_assign_code(
            ctx,
            operand,
            gen_sub_ir(ctx, operand, IntValue(operand.type, 1))
        )
        return operand

    else:
        raise Todo()

def gen_post_dec_ir(ctx, operand):
    if type(operand.type) is IntType:
        value = LlvmValue(operand.type, operand.get_llvm_value())

        gen_assign_code(
            ctx,
            operand,
            gen_sub_ir(ctx, operand, IntValue(operand.type, 1))
        )

        return value

    else:
        raise Todo()

def gen_bit_and_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.and_(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_bit_or_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.or_(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_bit_not_ir(ctx, operand):
    common_type = get_concrete_type(operand.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.not_(
                gen_implicit_cast_ir(
                    ctx, operand, common_type
                ).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_bit_xor_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.xor(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()

def gen_bit_shr_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        if common_type.is_signed:
            return LlvmValue(
                common_type,
                ctx.builder.ashr(
                    gen_implicit_cast_ir(
                        ctx, lhs, common_type
                    ).get_llvm_value(),
                    gen_implicit_cast_ir(
                        ctx, rhs, common_type
                    ).get_llvm_value()
                )
            )
        else:
            return LlvmValue(
                common_type,
                ctx.builder.lshr(
                    gen_implicit_cast_ir(
                        ctx, lhs, common_type
                    ).get_llvm_value(),
                    gen_implicit_cast_ir(
                        ctx, rhs, common_type
                    ).get_llvm_value()
                )
            )

    else:
        raise Todo()

def gen_bit_shl_ir(ctx, lhs, rhs):
    common_type = get_common_type(lhs.type, rhs.type)

    if type(common_type) is IntType:
        return LlvmValue(
            common_type,
            ctx.builder.shl(
                gen_implicit_cast_ir(ctx, lhs, common_type).get_llvm_value(),
                gen_implicit_cast_ir(ctx, rhs, common_type).get_llvm_value()
            )
        )

    else:
        raise Todo()
