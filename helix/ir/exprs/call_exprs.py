from ..types import *

from .cast_exprs import gen_implicit_cast_ir, get_concrete_type

def gen_call_ir(ctx, expr):
    from .exprs import gen_expr_ir

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

    elif value_type is BoundAttrFunValue:
        ir_args = [ lhs.instance.get_llvm_ptr() ]

        # add 1 for instance
        if len(expr.args) + 1 == len(lhs.type.param_types):
            for arg_node, param_type in zip(
                expr.args, lhs.type.param_types[1:]
            ):
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
        ctor = lhs.get_ctor_symbol()

        if ctor is not None:
            ctor_fun = ctor.ir_value
            value = StackValue(ctx, lhs)

            ir_args = [ value.get_llvm_ptr() ]

            # add 1 for instance
            if len(expr.args) == len(ctor_fun.type.param_types) - 1:
                for arg_node, param_type in zip(
                    expr.args, ctor_fun.type.param_types[1:]
                ):
                    ir_args.append(
                        gen_implicit_cast_ir(
                            ctx, gen_expr_ir(ctx, arg_node), param_type
                        ).get_llvm_value()
                    )

            else:
                raise Todo("arg length mismatch")

            ctx.builder.call(ctor_fun.get_llvm_value(), ir_args)

            return value

        else:
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
