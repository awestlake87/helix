from contextlib import contextmanager

from ..err import Todo
from ..ast import *

from .exprs import *
from .statements import *
from .types import *
from .values import *

def gen_unit_sym(unit_node):
    class Context:
        def __init__(self, unit_sym):
            self.unit = unit_sym

            self.scope = None

        @contextmanager
        def use_scope(self, scope):
            old_scope = self.scope
            self.scope = scope

            yield

            self.scope = old_scope

    unit_sym = UnitSym(unit_node.id, unit_node)

    ctx = Context(unit_sym)

    with ctx.use_scope(unit_sym.scope):
        unit_sym.block = gen_block_sym(ctx, unit_node.block)

    return unit_sym

def gen_block_sym(ctx, block_node):
    block_sym = BlockSym(ctx.scope)

    with ctx.use_scope(block_sym.scope):
        for statement in block_node.statements:
            block_sym.statements.append(gen_statement_sym(ctx, statement))

    return block_sym

def gen_statement_sym(ctx, statement_node):
    statement_type = type(statement_node)

    if issubclass(statement_type, ExprNode):
        return gen_expr_sym(ctx, statement_node)

    elif statement_type is ReturnNode:
        return gen_return_sym(ctx, statement_node)

    else:
        raise Todo(statement_type)

def gen_expr_sym(ctx, expr_node):
    expr_type = type(expr_node)

    if expr_type is InitNode:
        return gen_init_sym(ctx, expr_node)

    elif expr_type is AssignNode:
        return gen_assign_sym(ctx, expr_node)

    elif expr_type is SymbolNode:
        return SymbolSym(expr_node.id)

    elif expr_type is AutoIntNode:
        return AutoIntSym(expr_node.value, expr_node.radix)

    else:
        raise Todo(expr_type)


def gen_init_sym(ctx, init_node):
    lhs_type = type(init_node.lhs)

    if lhs_type is SymbolNode:
        ctx.scope.insert(init_node.lhs.id, VarSym())

        return InitSym(
            SymbolSym(init_node.lhs.id), gen_expr_sym(ctx, init_node.rhs)
        )

    else:
        raise Todo(lhs_type)

def gen_assign_sym(ctx, assign_node):
    return AssignSym(
        gen_expr_sym(ctx, assign_node.lhs), gen_expr_sym(ctx, assign_node.rhs)
    )

def gen_return_sym(ctx, return_node):
    if return_node.expr is not None:
        return ReturnSym(gen_expr_sym(ctx, return_node.expr))

    else:
        return ReturnSym()
