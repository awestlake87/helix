from contextlib import contextmanager

from ..err import Todo
from ..sym import *

def check_ownership(block_sym):
    class Context:
        def __init__(self):
            self.scope = None
            self.var_info = { }

        @contextmanager
        def use_scope(self, scope):
            old_scope = self.scope
            self.scope = scope

            yield

            self.scope = old_scope

        def get_var_info(self, var_sym):
            if var_sym in self.var_info:
                return self.var_info[var_sym]

            else:
                raise Todo()

    ctx = Context()

    with ctx.use_scope(block_sym.scope):
        for statement in block_sym.statements:
            check_statement_ownership(ctx, statement)

def check_statement_ownership(ctx, statement_sym):
    statement_type = type(statement_sym)

    if issubclass(statement_type, ExprSym):
        check_expr_ownership(ctx, statement_sym)

    elif statement_type is ReturnSym:
        check_return_ownership(ctx, statement_sym)

    else:
        raise Todo(statement_type)

def check_expr_ownership(ctx, expr_sym):
    expr_type = type(expr_sym)

    if expr_type is InitSym:
        check_init_ownership(ctx, expr_sym)

    elif expr_type is AssignSym:
        check_assign_ownership(ctx, expr_sym)

    elif expr_type is SymbolSym:
        pass

    else:
        raise Todo(expr_type)

def check_init_ownership(ctx, expr_sym):
    pass

def check_assign_ownership(ctx, expr_sym):
    pass

def check_return_ownership(ctx, return_sym):
    pass
