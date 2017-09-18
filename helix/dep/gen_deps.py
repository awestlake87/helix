
from ..err import *
from ..sym import *

def gen_expr_sym(ctx, expr):
    expr_type = type(expr)

    if expr_type is SymbolNode:
        return ctx.scope.resolve(expr.id)

    elif expr_type is GlobalNode:
        return ctx.scope.resolve(expr.id)

    elif expr_type is MutNode:
        return gen_expr_sym(ctx, expr.operand)

    elif expr_type is DotNode:
        lhs = gen_expr_sym(ctx, expr.lhs)

        if type(lhs) is VarSym or type(lhs) is GlobalSym:
            if type(lhs.type) is StructSym:
                if type(expr.rhs) is SymbolNode:
                    sym = lhs.type.get_attr_symbol(expr.rhs.id)

                    if type(sym) is StructSym:
                        return VarSym(sym)

                    else:
                        return sym

                else:
                    raise Todo()

    elif expr_type is CallNode:
        lhs = gen_expr_sym(ctx, expr.lhs)

        if type(lhs) is StructSym:
            return VarSym(lhs)

        else:
            return None

    else:
        return None


def gen_unit_deps(unit):
    class Context:
        def __init__(self, unit_sym):
            self.unit = unit_sym
            self.scope = None

        def get_scope(self, ast_node):
            return self.unit.get_scope(ast_node)

        @contextmanager
        def use_scope(self, scope):
            old_scope = self.scope
            self.scope = scope

            yield

            self.scope = old_scope

    ctx = Context(unit)

    jit_fun = FunSym(
        unit,
        unit.scope,
        FunTypeNode(BangNode(IntTypeNode(32, True)), [ ]),
        OperName(OperName.OP_JIT),
        [ ],
        unit.ast.block
    )

    gen_fun_deps(ctx, jit_fun)

    return [ jit_fun.target ]


def gen_block_deps(ctx, block):
    with ctx.use_scope(ctx.get_scope(block)):
        deps = [ ]
        for statement in block.statements:
            deps += gen_statement_deps(ctx, statement)

        return deps

def gen_statement_deps(ctx, statement):
    statement_type = type(statement)

    if statement_type is ReturnNode:
        return gen_return_deps(ctx, statement)

    elif statement_type is IfNode:
        return gen_if_deps(ctx, statement)

    elif statement_type is LoopNode:
        return gen_loop_deps(ctx, statement)

    elif statement_type is SwitchNode:
        return gen_switch_deps(ctx, statement)

    elif statement_type is TryNode:
        return gen_try_deps(ctx, statement)

    elif statement_type is ThrowNode:
        return gen_expr_deps(ctx, statement.expr)

    elif statement_type is BreakNode or statement_type is ContinueNode:
        return [ ]

    elif issubclass(statement_type, ExprNode):
        return gen_expr_deps(ctx, statement)

    elif statement_type is BlockNode:
        return gen_block_deps(ctx, statement)

    else:
        raise Todo(repr(statement))

def gen_expr_deps(ctx, expr):
    expr_type = type(expr)

    if expr_type is CallNode:
        return gen_call_deps(ctx, expr)

    elif expr_type is EmbedCallNode:
        return gen_call_deps(ctx, expr)

    elif expr_type is DotNode:
        return gen_dot_expr_deps(ctx, expr)

    elif expr_type is InitNode:
        return gen_init_expr_deps(ctx, expr)

    elif expr_type is TernaryConditionalNode:
        return gen_ternary_conditional_deps(ctx, expr)

    elif issubclass(expr_type, UnaryExprNode):
        return gen_unary_expr_deps(ctx, expr)

    elif issubclass(expr_type, BinaryExprNode):
        return gen_binary_expr_deps(ctx, expr)

    elif expr_type is StructNode:
        return gen_struct_deps(ctx, expr)

    elif expr_type is FunNode:
        return gen_fun_deps(ctx, ctx.scope.resolve(expr.id))

    elif expr_type is SymbolNode:
        sym = ctx.scope.resolve(expr.id)

        if type(sym) is FunSym:
            return [ sym.proto_target ]

        elif sym.target is not None:
            return [ sym.target ]

        else:
            return [ ]

    elif expr_type is FunTypeNode:
        return gen_fun_type_deps(ctx, expr)
    elif expr_type is IntTypeNode:
        return [ ]
    elif expr_type is AttrNode:
        return [ ]
    elif expr_type is VoidTypeNode:
        return [ ]
    elif expr_type is AutoTypeNode:
        return [ ]
    elif expr_type is ArrayTypeNode:
        return (
            gen_expr_deps(ctx, expr.length) +
            gen_expr_deps(ctx, expr.type)
        )

    elif expr_type is GlobalNode:
        return gen_global_deps(ctx, expr)

    elif expr_type is AutoIntNode:
        return [ ]
    elif expr_type is IntNode:
        return [ ]
    elif expr_type is StringNode:
        return [ ]
    elif expr_type is NilNode:
        return [ ]

    else:
        raise Todo(expr)

def gen_struct_deps(ctx, expr):
    symbol = ctx.scope.resolve(expr.id)

    for attr_id, attr_symbol in symbol.attrs:
        attr_type = type(attr_symbol)

        if attr_type is DataAttrSym:
            symbol.target.deps += gen_expr_deps(
                ctx, attr_symbol.ast.type
            )
            symbol.target.attrs[attr_id] = attr_symbol

        elif issubclass(attr_type, AttrFunSym):
            symbol.target.attrs[attr_id] = attr_symbol

        else:
            raise Todo()

    return [ ]

def gen_fun_deps(ctx, symbol):
    symbol.proto_target.deps += gen_expr_deps(ctx, symbol.type)

    if symbol.body is not None:
        with ctx.use_scope(symbol.scope):
            symbol.target.deps += gen_block_deps(ctx, symbol.body)

    return [ ]

def gen_global_deps(ctx, expr):
    symbol = ctx.scope.resolve(expr.id)

    symbol.target.deps += gen_expr_deps(ctx, expr.type)

    if symbol.init_expr is not None:
        symbol.target.deps += gen_expr_deps(ctx, symbol.init_expr)

    return [ ]


def gen_unary_expr_deps(ctx, expr):
    return gen_expr_deps(ctx, expr.operand)

def gen_binary_expr_deps(ctx, expr):
    return gen_expr_deps(ctx, expr.lhs) + gen_expr_deps(ctx, expr.rhs)

def gen_dot_expr_deps(ctx, expr):
    deps = [ ]

    lhs = gen_expr_sym(ctx, expr.lhs)

    if type(lhs) is GlobalSym:
        deps.append(lhs.target)

    sym = gen_expr_sym(ctx, expr)

    if type(sym) is AttrFunSym:
        deps.append(sym.target)

    elif type(sym) is GlobalSym:
        deps.append(sym.target)

    return deps

def gen_init_expr_deps(ctx, expr):
    deps = gen_expr_deps(ctx, expr.lhs) + gen_expr_deps(ctx, expr.rhs)

    lhs = gen_expr_sym(ctx, expr.lhs)
    rhs = gen_expr_sym(ctx, expr.rhs)

    if lhs is None:
        raise Todo()

    if type(rhs) is VarSym:
        lhs.type = rhs.type

    elif type(rhs) is GlobalSym:
        lhs.type = rhs.type

    return deps

def gen_ternary_conditional_deps(ctx, expr):
    return (
        gen_expr_deps(ctx, expr.lhs) +
        gen_expr_deps(ctx, expr.condition) +
        gen_expr_deps(ctx, expr.rhs)
    )

def gen_call_deps(ctx, expr):
    deps = gen_expr_deps(ctx, expr.lhs)

    lhs = gen_expr_sym(ctx, expr.lhs)

    if type(lhs) is StructSym:
        ctor = lhs.get_ctor_symbol()
        dtor = lhs.get_dtor_symbol()

        if ctor is not None:
            deps.append(ctor.target)

        if dtor is not None:
            deps.append(dtor.target)

    elif type(lhs) is FunSym or type(lhs) is AttrFunSym:
        if lhs.target is not None:
            ctx.unit.target.deps.append(lhs.target)

    return deps

def gen_fun_type_deps(ctx, fun_type):
    deps = gen_expr_deps(ctx, fun_type.ret_type)

    for param in fun_type.param_types:
        if type(param) is BangNode:
            deps += gen_expr_deps(ctx, param.operand)

        else:
            raise Todo()

    return deps

def gen_return_deps(ctx, statement):
    if statement.expr is not None:
        return gen_expr_deps(ctx, statement.expr)

    else:
        return [ ]

def gen_if_deps(ctx, statement):
    deps = [ ]

    with ctx.use_scope(ctx.get_scope(statement)):
        for condition, block in statement.if_branches:
            deps += gen_expr_deps(ctx, condition)
            deps += gen_block_deps(ctx, block)

        if statement.else_block is not None:
            deps += gen_block_deps(ctx, statement.else_block)

    return deps

def gen_loop_deps(ctx, statement):
    deps = [ ]

    with ctx.use_scope(ctx.get_scope(statement)):
        if statement.for_clause is not None:
            deps += gen_expr_deps(ctx, statement.for_clause)

        if statement.each_clause is not None:
            deps += gen_expr_deps(ctx, statement.each_clause)

        if statement.while_clause is not None:
            deps += gen_expr_deps(ctx, statement.while_clause)

        if statement.loop_body is not None:
            deps += gen_block_deps(ctx, statement.loop_body)

        if statement.then_clause is not None:
            deps += gen_expr_deps(ctx, statement.then_clause)

        if statement.until_clause is not None:
            deps += gen_expr_deps(ctx, statement.until_clause)

    return deps

def gen_switch_deps(ctx, statement):
    deps = [ ]

    with ctx.use_scope(ctx.get_scope(statement)):
        for case_values, case_block in statement.case_branches:
            for value in case_values:
                deps += gen_expr_deps(ctx, value)
            deps += gen_block_deps(ctx, case_block)

        if statement.default_block is not None:
            deps += gen_block_deps(ctx, statement.default_block)

    return deps

def gen_try_deps(ctx, statement):
    deps = gen_block_deps(ctx, statement.try_block)

    for clause in statement.catch_clauses:
        with ctx.use_scope(ctx.get_scope(clause)):
            deps += gen_expr_deps(ctx, clause.type)
            deps += gen_block_deps(ctx, clause.block)

    if statement.default_catch is not None:
        deps += gen_block_deps(ctx, statement.default_catch)

    return deps
