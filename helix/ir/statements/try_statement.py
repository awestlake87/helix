from llvmlite import ir

from ..types import IntType, PtrType, LlvmValue

from ..exprs import (
    gen_expr_ir,
    gen_implicit_cast_ir,
    gen_cast_ir,
    get_concrete_type,
    get_rtti_info,
    gen_sizeof_ir
)

def gen_try_code(ctx, statement):
    from .statements import gen_block_code

    lpad_block = ctx.builder.append_basic_block("lpad")
    try_end = ctx.builder.append_basic_block("try_end")

    try_control_path = ctx.control_path.fork()

    with ctx.use_control_path(try_control_path):
        with ctx.use_try_context(lpad_block):
            gen_block_code(ctx, statement.try_block)

            if not ctx.builder.block.is_terminated:
                ctx.builder.branch(try_end)

        personality = None

        try:
            personality = ctx.builder.module.get_global("__gxx_personality_v0")

        except KeyError as e:
            personality = ir.Function(
                ctx.builder.module,
                ir.FunctionType(ir.IntType(32), [ ], True),
                "__gxx_personality_v0"
            )

        ctx.builder.function.attributes.personality = personality

        eh_for_intrinsic = None

        try:
            eh_for_intrinsic = ctx.builder.module.get_global(
                "llvm.eh.typeid.for"
            )
        except KeyError as e:
            eh_for_intrinsic = ir.Function(
                ctx.builder.module,
                ir.FunctionType(
                    ir.IntType(32),
                    [ ir.IntType(8).as_pointer() ]
                ),
                "llvm.eh.typeid.for"
            )

        begin_catch = None

        try:
            begin_catch = ctx.builder.module.get_global(
                "__cxa_begin_catch"
            )

        except KeyError as e:
            begin_catch = ir.Function(
                ctx.builder.module,
                ir.FunctionType(
                    ir.IntType(8).as_pointer(),
                    [ ir.IntType(8).as_pointer() ]
                ),
                "__cxa_begin_catch"
            )

        ctx.builder.position_at_start(lpad_block)
        lpad = ctx.builder.landingpad(
            ir.LiteralStructType(
                [ ir.IntType(8).as_pointer(), ir.IntType(32) ]
            )
        )
        lpad_value = ctx.builder.extract_value(lpad, 1)

        lpad_elif_block = None

        def create_cleanup_block(ctx, next_block):
            end_catch = None

            try:
                end_catch = ctx.builder.module.get_global(
                    "__cxa_end_catch"
                )

            except KeyError as e:
                end_catch = ir.Function(
                    ctx.builder.module,
                    ir.FunctionType(ir.VoidType(), [ ]),
                    "__cxa_end_catch"
                )

            block = ctx.builder.append_basic_block("catch_cleanup")

            with ctx.builder.goto_block(block):
                ctx.builder.call(end_catch, [ ])
                ctx.builder.branch(next_block)

            return block

        for clause in statement.catch_clauses:
            catch_type = gen_expr_ir(ctx, clause.type)
            type_info = None

            if type(catch_type) is PtrType:
                type_info = get_rtti_info(ctx, catch_type.pointee)

            else:
                raise Todo(catch_type)

            lpad.add_clause(ir.CatchClause(type_info))

            cmp_value = ctx.builder.call(
                eh_for_intrinsic,
                [
                    ctx.builder.bitcast(
                        type_info, ir.IntType(8).as_pointer()
                    )
                ]
            )

            catch_block = ctx.builder.append_basic_block("catch")
            lpad_elif_block = ctx.builder.append_basic_block("lpad_elif")

            ctx.builder.cbranch(
                ctx.builder.icmp_unsigned("==", lpad_value, cmp_value),
                catch_block,
                lpad_elif_block
            )

            ctx.builder.position_at_start(catch_block)

            e_value = ctx.builder.extract_value(lpad, 0)

            e_ptr = ctx.builder.call(
                begin_catch, [ e_value ]
            )

            if type(catch_type) is PtrType:
                clause.scope.resolve(clause.id).ir_value = LlvmValue(
                    catch_type,
                    ctx.builder.bitcast(
                        e_ptr, catch_type.get_llvm_value()
                    )
                )

            catch_control_path = ctx.control_path.fork()
            catch_control_path.will_need_cleanup = True

            catch_control_path.push_cleanup(create_cleanup_block)

            with ctx.use_control_path(catch_control_path):
                with ctx.use_scope(ctx.get_scope(clause)):
                    gen_block_code(ctx, clause.block)

            if not catch_control_path.is_terminated:
                ctx.builder.branch(try_end)


            ctx.builder.position_at_start(lpad_elif_block)

        if statement.default_catch is not None:
            lpad.add_clause(ir.CatchClause(ir.IntType(8).as_pointer()(None)))

            e_value = ctx.builder.extract_value(lpad, 0)
            e_ptr = ctx.builder.call(
                begin_catch, [ e_value ]
            )

            catch_control_path = ctx.control_path.fork()
            catch_control_path.will_need_cleanup = True

            catch_control_path.push_cleanup(create_cleanup_block)

            with ctx.use_control_path(catch_control_path):
                gen_block_code(ctx, statement.default_catch)

            if not catch_control_path.is_terminated:
                ctx.builder.branch(try_end)

        else:
            ctx.builder.resume(lpad)

        ctx.builder.position_at_start(try_end)

    if try_control_path.is_terminated:
        ctx.builder.branch(ctx.unreachable)


def gen_throw_code(ctx, statement):
    throw_value = gen_expr_ir(ctx, statement.expr)
    throw_value = gen_implicit_cast_ir(
        ctx, throw_value, get_concrete_type(throw_value.type)
    )

    alloc_exception = None
    throw_exception = None

    try:
        alloc_exception = ctx.builder.module.get_global(
            "__cxa_allocate_exception"
        )

    except KeyError as e:
        alloc_exception = ir.Function(
            ctx.builder.module,
            ir.FunctionType(
                ir.IntType(8).as_pointer(),
                [ ir.IntType(64) ]
            ),
            "__cxa_allocate_exception"
        )

    try:
        throw_exception = ctx.builder.module.get_global(
            "__cxa_throw"
        )

    except KeyError as e:
        throw_exception = ir.Function(
            ctx.builder.module,
            ir.FunctionType(
                ir.VoidType(),
                [
                    ir.IntType(8).as_pointer(),
                    ir.IntType(8).as_pointer(),
                    ir.IntType(8).as_pointer()
                ]
            ),
            "__cxa_throw"
        )

    type_info = get_rtti_info(ctx, throw_value.type)
    exception_buffer = ctx.builder.call(
        alloc_exception,
        [
            gen_cast_ir(
                ctx,
                gen_sizeof_ir(ctx, throw_value), IntType(64)
            ).get_llvm_value()
        ]
    )

    ctx.builder.store(
        throw_value.get_llvm_value(),
        ctx.builder.bitcast(
            exception_buffer, PtrType(throw_value.type).get_llvm_value()
        )
    )


    assert type_info is not None
    assert exception_buffer is not None

    throw_args = [
        exception_buffer,
        ctx.builder.bitcast(type_info, ir.IntType(8).as_pointer()),
        ir.IntType(8).as_pointer()(None)
    ]

    if ctx.try_context is not None:
        ctx.builder.invoke(
            throw_exception,
            throw_args,
            ctx.unreachable,
            ctx.try_context.unwind_to
        )

    else:
        ctx.builder.call(throw_exception, throw_args)

    ctx.control_path.is_terminated = True
