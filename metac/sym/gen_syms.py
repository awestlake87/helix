from contextlib import contextmanager

from ..ast import *
from ..err import Todo

from .exprs import *
from .statements import *
from .types import *
from .values import *

def gen_unit_sym(unit_node):
    class Context:
        def __init__(self, unit):
            self.unit = unit
            self.scope = None

        @contextmanager
        def use_scope(self, scope):
            old_scope = self.scope
            self.scope = scope

            yield

            self.scope = old_scope

    unit_sym = UnitSym()
    ctx = Context(unit_sym)

    with ctx.use_scope(unit_sym.scope):
        unit_sym.block = gen_block_sym(ctx, unit_node)

    return unit_sym

def gen_block_sym(ctx, block_node):
    block_sym = BlockSym(ctx.scope)

    with ctx.use_scope(block_sym.scope):
        for statement in block_node.statements:
            block_sym.statements.append(gen_statement_sym(ctx, statement))

    return block_sym

def gen_statement_sym(ctx, statement_node):
    statement_type = type(statement_node)

    if statement_type is ReturnNode:
        return gen_return_sym(ctx, statement_node)

    elif statement_type is IfNode:
        return gen_if_sym(ctx, statement_node)

    elif statement_type is LoopNode:
        return gen_loop_sym(ctx, statement_node)

    elif statement_type is SwitchNode:
        return gen_switch_sym(ctx, statement_node)

    elif statement_type is BreakNode:
        return BreakSym()

    elif statement_type is ContinueNode:
        return ContinueSym()

    elif issubclass(statement_type, ExprNode):
        return gen_expr_sym(ctx, statement_node)

    else:
        raise Todo(statement_type)

def gen_expr_sym(ctx, expr_node):
    expr_type = type(expr_node)

    if expr_type is CallNode:
        return gen_call_sym(ctx, expr_node)

    elif expr_type is InitNode:
        return gen_init_sym(ctx, expr_node)

    elif issubclass(expr_type, BinaryNode):
        return gen_binary_expr_sym(ctx, expr_node)

    elif issubclass(expr_type, UnaryNode):
        return gen_unary_expr_sym(ctx, expr_node)

    elif expr_type is FunNode:
        return gen_fun_sym(ctx, expr_node)

    elif expr_type is SymbolNode:
        return SymbolSym(expr_node.id)

    elif expr_type is AutoIntNode:
        return AutoIntSym(expr_node.value, expr_node.radix)

    elif expr_type is IntNode:
        return IntSym(
            expr_node.num_bits,
            expr_node.is_signed,
            expr_node.value,
            expr_node.radix
        )

    elif expr_type is FunTypeNode:
        return gen_fun_type_sym(ctx, expr_node)

    elif expr_type is IntTypeNode:
        return gen_int_type_sym(ctx, expr_node)

    else:
        raise Todo(expr_type)

def gen_unary_expr_sym(ctx, expr_node):
    expr_type = type(expr_node)

    operand = gen_expr_sym(ctx, expr_node.operand)

    if expr_type is PreIncNode:
        return PreIncSym(operand)

    elif expr_type is PostIncNode:
        return PostIncSym(operand)

    elif expr_type is PreDecNode:
        return PreDecSym(operand)

    elif expr_type is PostDecNode:
        return PostDecSym(operand)

    elif expr_type is NegNode:
        return NegSym(operand)

    elif expr_type is NotNode:
        return NotSym(operand)

    elif expr_type is BitNotNode:
        return BitNotSym(operand)

    else:
        raise Todo(expr_type)

def gen_binary_expr_sym(ctx, expr_node):
    expr_type = type(expr_node)

    lhs = gen_expr_sym(ctx, expr_node.lhs)
    rhs = gen_expr_sym(ctx, expr_node.rhs)

    if expr_type is AssignNode:
        return AssignSym(lhs, rhs)


    elif expr_type is LtnNode:
        return LtnSym(lhs, rhs)

    elif expr_type is GtnNode:
        return GtnSym(lhs, rhs)

    elif expr_type is LeqNode:
        return LeqSym(lhs, rhs)

    elif expr_type is GeqNode:
        return GeqSym(lhs, rhs)

    elif expr_type is EqlNode:
        return EqlSym(lhs, rhs)

    elif expr_type is NeqNode:
        return NeqSym(lhs, rhs)


    elif expr_type is AndNode:
        return AndSym(lhs, rhs)

    elif expr_type is OrNode:
        return OrSym(lhs, rhs)

    elif expr_type is XorNode:
        return XorSym(lhs, rhs)


    elif expr_type is AddNode:
        return AddSym(lhs, rhs)

    elif expr_type is SubNode:
        return SubSym(lhs, rhs)

    elif expr_type is MulNode:
        return MulSym(lhs, rhs)

    elif expr_type is DivNode:
        return DivSym(lhs, rhs)

    elif expr_type is ModNode:
        return ModSym(lhs, rhs)
        

    elif expr_type is BitAndNode:
        return BitAndSym(lhs, rhs)

    elif expr_type is BitOrNode:
        return BitOrSym(lhs, rhs)

    elif expr_type is BitXorNode:
        return BitXorSym(lhs, rhs)

    elif expr_type is BitShlNode:
        return BitShlSym(lhs, rhs)

    elif expr_type is BitShrNode:
        return BitShrSym(lhs, rhs)

    else:
        raise Todo(expr_type)

def gen_return_sym(ctx, return_node):
    return ReturnSym(gen_expr_sym(ctx, return_node.expr))

def gen_if_sym(ctx, if_node):
    if_sym = IfSym(ctx.scope)

    with ctx.use_scope(if_sym.scope):
        for condition, block in if_node.if_branches:
            if_sym.if_branches.append(
                (gen_expr_sym(ctx, condition), gen_block_sym(ctx, block))
            )

        if if_node.else_block is not None:
            if_sym.else_block = gen_block_sym(ctx, if_node.else_block)

    return if_sym

def gen_loop_sym(ctx, loop_node):
    loop_sym = LoopSym(ctx.scope)

    with ctx.use_scope(loop_sym.scope):
        if loop_node.for_clause is not None:
            loop_sym.for_clause = gen_expr_sym(ctx, loop_node.for_clause)

        if loop_node.each_clause is not None:
            loop_sym.each_clause = gen_expr_sym(ctx, loop_node.each_clause)

        if loop_node.while_clause is not None:
            loop_sym.while_clause = gen_expr_sym(ctx, loop_node.while_clause)

        if loop_node.loop_body is not None:
            loop_sym.loop_body = gen_block_sym(ctx, loop_node.loop_body)

        if loop_node.then_clause is not None:
            loop_sym.then_clause = gen_expr_sym(ctx, loop_node.then_clause)

        if loop_node.until_clause is not None:
            loop_sym.until_clause = gen_expr_sym(ctx, loop_node.until_clause)

    return loop_sym

def gen_switch_sym(ctx, switch_node):
    switch_sym = SwitchSym(ctx.scope)

    switch_sym.value = gen_expr_sym(ctx, switch_node.value)

    with ctx.use_scope(switch_sym.scope):
        for case_values, case_block in switch_node.case_branches:
            case_value_syms = [ ]

            for value in case_values:
                case_value_syms.append(gen_expr_sym(ctx, value))

            switch_sym.case_branches.append(
                (case_value_syms, gen_block_sym(ctx, case_block))
            )

        if switch_node.default_block is not None:
            switch_sym.default_block = gen_block_sym(
                ctx, switch_node.default_block
            )

    return switch_sym


def gen_call_sym(ctx, call_expr_node):
    return CallSym(
        gen_expr_sym(ctx, call_expr_node.lhs),
        [ gen_expr_sym(ctx, arg_node) for arg_node in call_expr_node.args ]
    )

def gen_init_sym(ctx, expr):
    lhs_type = type(expr.lhs)

    if lhs_type is SymbolNode:
        lhs = SymbolSym(expr.lhs.id)
        rhs = gen_expr_sym(ctx, expr.rhs)

        ctx.scope.insert(lhs.id, lhs)

        return InitSym(lhs, rhs)

    else:
        raise Todo(lhs_type)

def gen_fun_sym(ctx, fun_node):
    fun_type_sym = gen_expr_sym(ctx, fun_node.type)

    fun_sym = FunSym(
        ctx.scope,
        fun_node.id,
        fun_type_sym,
        fun_node.param_ids,
        is_cfun = fun_node.is_cfun
    )
    ctx.scope.insert(fun_node.id, fun_sym)

    with ctx.use_scope(fun_sym.scope):
        for param_id in fun_node.param_ids:
            ctx.scope.insert(param_id, VarSym())

        if fun_node.body is not None:
            fun_sym.body = gen_block_sym(ctx, fun_node.body)

    return fun_sym

def gen_fun_type_sym(ctx, fun_type_node):
    return FunTypeSym(
        gen_expr_sym(ctx, fun_type_node.ret_type),
        [
            gen_expr_sym(ctx, param_node)
            for param_node in
            fun_type_node.param_types
        ]
    )

def gen_int_type_sym(ctx, int_type_node):
    return IntTypeSym(int_type_node.num_bits, int_type_node.is_signed)
