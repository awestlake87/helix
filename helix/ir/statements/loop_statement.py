
from ..exprs import gen_expr_ir, gen_as_bit_ir

def gen_loop_code(ctx, statement):
    from .statements import gen_block_code

    control_path = ctx.control_path.fork()

    with ctx.use_control_path(control_path):
        with ctx.use_scope(ctx.get_scope(statement)):
            if statement.for_clause is not None:
                gen_expr_ir(ctx, statement.for_clause)

            if statement.each_clause is not None:
                raise Todo("each clause")

            loop_head = None
            loop_body = ctx.builder.append_basic_block("loop_body")
            loop_then = ctx.builder.append_basic_block("loop_then")
            loop_exit = ctx.builder.append_basic_block("loop_exit")

            if statement.while_clause is not None:
                loop_head = ctx.builder.append_basic_block("loop_head")

                with ctx.builder.goto_block(loop_head):
                    ctx.builder.cbranch(
                        gen_as_bit_ir(
                            ctx, gen_expr_ir(ctx, statement.while_clause)
                        ).get_llvm_value(),
                        loop_body,
                        loop_exit
                    )
            else:
                loop_head = loop_body

            ctx.builder.branch(loop_head)

            ctx.builder.position_at_start(loop_body)
            with ctx.use_loop_context(loop_then, loop_exit):
                gen_block_code(ctx, statement.loop_body)

            if not ctx.builder.block.is_terminated:
                ctx.builder.branch(loop_then)


            with ctx.builder.goto_block(loop_then):
                if statement.then_clause is not None:
                    gen_expr_ir(ctx, statement.then_clause)

                if statement.until_clause is not None:
                    ctx.builder.cbranch(
                        gen_as_bit_ir(
                            ctx, gen_expr_ir(ctx, statement.until_clause)
                        ).get_llvm_value(),
                        loop_exit,
                        loop_head
                    )
                else:
                    ctx.builder.branch(loop_head)

                if not loop_then.is_terminated:
                    ctx.builder.branch(loop_exit)

            ctx.builder.position_at_start(loop_exit)


def gen_break_code(ctx, _):
    if ctx.loop_context is None:
        raise Todo()

    ctx.builder.branch(ctx.loop_context.loop_exit)

def gen_continue_code(ctx, _):
    if ctx.loop_context is None:
        raise Todo()

    ctx.builder.branch(ctx.loop_context.loop_then)
