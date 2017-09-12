from ..exprs import gen_expr_ir

from ...err import ReturnTypeMismatch, Todo

def gen_return_code(ctx, statement):
    if statement.expr is not None:
        value = gen_expr_ir(ctx, statement.expr)

        try:
            ctx.create_return(value)

        except Exception as e:
            raise ReturnTypeMismatch()

        ctx.control_path.is_terminated = True
    else:
        ctx.create_return()
