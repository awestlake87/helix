from ..types import IntType

from ..exprs import gen_implicit_cast_ir, gen_expr_ir, get_concrete_type


def gen_switch_code(ctx, statement):
    from .statements import gen_block_code

    assert statement.scope is not None

    control_path = ctx.control_path.fork()

    with ctx.use_control_path(control_path):
        with ctx.use_scope(statement.scope):
            value = gen_expr_ir(ctx, statement.value)
            concrete_type = get_concrete_type(value.type)

            if type(concrete_type) is IntType:
                default_block = ctx.builder.append_basic_block("default")

                inst = ctx.builder.switch(
                    gen_implicit_cast_ir(
                        ctx, value, concrete_type
                    ).get_llvm_value(),
                    default_block
                )

                for case_values, case_block in statement.case_branches:
                    block = ctx.builder.append_basic_block("case")

                    for expr in case_values:
                        value = gen_implicit_cast_ir(
                            ctx, gen_expr_ir(ctx, expr), concrete_type
                        )

                        inst.add_case(
                            value.get_llvm_value(),
                            block
                        )

                    with ctx.builder.goto_block(block):
                        gen_block_code(ctx, case_block)

                with ctx.builder.goto_block(default_block):
                    gen_block_code(ctx, statement.default_block)

            else:
                raise Todo("non-integer switches")
