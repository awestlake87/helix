from ..exprs import gen_expr_ir, gen_as_bit_ir

def gen_if_statement_code(ctx, statement):
    from .statements import gen_block_code
    
    assert statement.scope is not None

    if_control_path = ctx.control_path.fork()

    with ctx.use_control_path(if_control_path):
        with ctx.use_scope(statement.scope):
            assert len(statement.if_branches) >= 1

            end_if = ctx.builder.append_basic_block("end_if")
            then_block = ctx.builder.append_basic_block("then")
            else_block = ctx.builder.append_basic_block("else")

            num = len(statement.if_branches)

            for branch in statement.if_branches:
                condition, block = branch

                ctx.builder.cbranch(
                    gen_as_bit_ir(
                        ctx, gen_expr_ir(ctx, condition)
                    ).get_llvm_value(),
                    then_block,
                    else_block
                )

                ctx.builder.position_at_start(then_block)
                gen_block_code(ctx, block)

                if not ctx.builder.block.is_terminated:
                    ctx.builder.branch(end_if)

                ctx.builder.position_at_start(else_block)

                if branch is not statement.if_branches[-1]:
                    then_block = ctx.builder.append_basic_block("then")
                    else_block = ctx.builder.append_basic_block("else")

            ctx.builder.position_at_start(else_block)

            if statement.else_block is not None:
                gen_block_code(ctx, statement.else_block)

            else:
                # need empty control path so parent control path knows it
                # didn't terminate
                ctx.control_path.fork()

            if not ctx.builder.block.is_terminated:
                ctx.builder.branch(end_if)

        ctx.builder.position_at_start(end_if)

    if if_control_path.is_terminated:
        ctx.builder.branch(ctx.unreachable)
