from ..exprs import gen_expr_ir

from ...err import ReturnTypeMismatch

def gen_return_statement_code(ctx, statement):
    value = gen_expr_ir(ctx, statement.expr)

    try:
        ctx.create_return(value)

    except Exception as e:
        raise ReturnTypeMismatch()

    ctx.control_path.is_terminated = True
