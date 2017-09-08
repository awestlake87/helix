
from ..err import *
from ..sym import *

def gen_expr_sym(unit, expr):
    expr_type = type(expr)

    if expr_type is SymbolSym:
        return unit.scope.resolve(expr.id)

    elif expr_type is GlobalSym:
        return unit.scope.resolve(expr.id)

    elif expr_type is DotSym:
        lhs = gen_expr_sym(unit, expr.lhs)

        if type(lhs) is VarSym or type(lhs) is GlobalSym:
            if type(lhs.type) is StructSym:
                if type(expr.rhs) is SymbolSym:
                    sym = lhs.type.get_attr_symbol(expr.rhs.id)

                    if type(sym) is StructSym:
                        return VarSym(sym)

                    else:
                        return sym

                else:
                    raise Todo()

    elif expr_type is CallSym:
        lhs = gen_expr_sym(unit, expr.lhs)

        if type(lhs) is StructSym:
            return VarSym(lhs)

        else:
            return None

    else:
        return None


def gen_unit_deps(unit):
    jit_fun = FunSym(
        unit,
        unit.scope,
        FunTypeSym(BangSym(IntTypeSym(32, True)), [ ]),
        OperName(OperName.OP_JIT),
        [ ],
        unit.block
    )

    gen_fun_deps(unit, jit_fun)

    return [ jit_fun.target ]


def gen_block_deps(unit, block):
    assert block.scope is not None

    with unit.use_scope(block.scope):
        deps = [ ]
        for statement in block.statements:
            deps += gen_statement_deps(unit, statement)

        return deps

def gen_statement_deps(unit, statement):
    statement_type = type(statement)

    if statement_type is ReturnSym:
        return gen_return_deps(unit, statement)

    elif statement_type is IfSym:
        return gen_if_deps(unit, statement)

    elif statement_type is LoopSym:
        return gen_loop_deps(unit, statement)

    elif statement_type is SwitchSym:
        return gen_switch_deps(unit, statement)

    elif statement_type is TrySym:
        return gen_try_deps(unit, statement)

    elif statement_type is ThrowSym:
        return gen_expr_deps(unit, statement.expr)

    elif statement_type is BreakSym or statement_type is ContinueSym:
        return [ ]

    elif issubclass(statement_type, ExprSym):
        return gen_expr_deps(unit, statement)

    elif statement_type is BlockSym:
        return gen_block_deps(unit, statement)

    else:
        raise Todo(repr(statement))

def gen_expr_deps(unit, expr):
    expr_type = type(expr)

    if expr_type is CallSym:
        return gen_call_deps(unit, expr)

    elif expr_type is EmbedCallSym:
        return gen_call_deps(unit, expr)

    elif expr_type is DotSym:
        return gen_dot_expr_deps(unit, expr)

    elif expr_type is InitSym:
        return gen_init_expr_deps(unit, expr)

    elif expr_type is TernaryConditionalSym:
        return gen_ternary_conditional_deps(unit, expr)

    elif issubclass(expr_type, UnaryExprSym):
        return gen_unary_expr_deps(unit, expr)

    elif issubclass(expr_type, BinaryExprSym):
        return gen_binary_expr_deps(unit, expr)

    elif expr_type is StructSym:
        return gen_struct_deps(unit, expr)

    elif expr_type is FunSym:
        return gen_fun_deps(unit, unit.scope.resolve(expr.id))

    elif expr_type is SymbolSym:
        sym = unit.scope.resolve(expr.id)

        if type(sym) is FunSym:
            return [ sym.proto_target ]

        else:
            return [ sym.target ]

    elif expr_type is FunTypeSym:
        return gen_fun_type_deps(unit, expr)

    elif expr_type is IntTypeSym:
        return [ ]

    elif expr_type is AttrSym:
        return [ ]

    elif expr_type is VoidTypeSym:
        return [ ]

    elif expr_type is AutoTypeSym:
        return [ ]

    elif expr_type is ArrayTypeSym:
        return (
            gen_expr_deps(unit, expr.length) +
            gen_expr_deps(unit, expr.type)
        )

    elif expr_type is GlobalSym:
        return gen_global_deps(unit, expr)

    elif issubclass(expr_type, LiteralSym):
        return [ ]

    else:
        raise Todo(expr)

def gen_struct_deps(unit, expr):
    symbol = unit.scope.resolve(expr.id)

    for attr_id, attr_symbol in symbol.attrs:
        attr_type = type(attr_symbol)

        if attr_type is DataAttrSym:
            symbol.target.deps += gen_expr_deps(
                unit, attr_symbol.ast.type
            )
            symbol.target.attrs[attr_id] = attr_symbol

        elif issubclass(attr_type, AttrFunSym):
            symbol.target.attrs[attr_id] = attr_symbol

        else:
            raise Todo()

    return [ ]

def gen_fun_deps(unit, symbol):
    symbol.proto_target.deps += gen_expr_deps(unit, symbol.type)

    if symbol.body is not None:
        with unit.use_scope(symbol.scope):
            symbol.target.deps += gen_block_deps(unit, symbol.body)

    return [ ]

def gen_global_deps(unit, expr):
    symbol = unit.scope.resolve(expr.id)

    symbol.target.deps += gen_expr_deps(unit, expr.type)

    if symbol.init_expr is not None:
        symbol.target.deps += gen_expr_deps(unit, symbol.init_expr)

    return [ ]


def gen_unary_expr_deps(unit, expr):
    return gen_expr_deps(unit, expr.operand)

def gen_binary_expr_deps(unit, expr):
    return gen_expr_deps(unit, expr.lhs) + gen_expr_deps(unit, expr.rhs)

def gen_dot_expr_deps(unit, expr):
    deps = [ ]

    lhs = gen_expr_sym(unit, expr.lhs)

    if type(lhs) is GlobalSym:
        deps.append(lhs.target)

    sym = gen_expr_sym(unit, expr)

    if type(sym) is AttrFunSym:
        deps.append(sym.target)

    elif type(sym) is GlobalSym:
        deps.append(sym.target)

    return deps

def gen_init_expr_deps(unit, expr):
    deps = gen_expr_deps(unit, expr.lhs) + gen_expr_deps(unit, expr.rhs)

    lhs = gen_expr_sym(unit, expr.lhs)
    rhs = gen_expr_sym(unit, expr.rhs)

    if type(rhs) is VarSym:
        lhs.type = rhs.type

    elif type(rhs) is GlobalSym:
        lhs.type = rhs.type

    return deps

def gen_ternary_conditional_deps(unit, expr):
    return (
        gen_expr_deps(unit, expr.lhs) +
        gen_expr_deps(unit, expr.condition) +
        gen_expr_deps(unit, expr.rhs)
    )

def gen_call_deps(unit, expr):
    deps = gen_expr_deps(unit, expr.lhs)

    lhs = gen_expr_sym(unit, expr.lhs)

    if type(lhs) is StructSym:
        ctor = lhs.get_ctor_symbol()
        dtor = lhs.get_dtor_symbol()

        if ctor is not None:
            deps.append(ctor.target)

        if dtor is not None:
            deps.append(dtor.target)

    elif type(lhs) is FunSym or type(lhs) is AttrFunSym:
        if lhs.target is not None:
            unit.target.deps.append(lhs.target)

    return deps

def gen_fun_type_deps(unit, fun_type):
    deps = gen_expr_deps(unit, fun_type.ret_type)

    for param in fun_type.param_types:
        if type(param) is BangSym:
            deps += gen_expr_deps(unit, param.operand)

        else:
            raise Todo()

    return deps

def gen_return_deps(unit, statement):
    if statement.expr is not None:
        return gen_expr_deps(unit, statement.expr)

    else:
        return [ ]

def gen_if_deps(unit, statement):
    assert statement.scope is not None

    deps = [ ]

    with unit.use_scope(statement.scope):
        for condition, block in statement.if_branches:
            deps += gen_expr_deps(unit, condition)
            deps += gen_block_deps(unit, block)

        if statement.else_block is not None:
            deps += gen_block_deps(unit, statement.else_block)

    return deps

def gen_loop_deps(unit, statement):
    assert statement.scope is not None

    deps = [ ]

    with unit.use_scope(statement.scope):
        if statement.for_clause is not None:
            deps += gen_expr_deps(unit, statement.for_clause)

        if statement.each_clause is not None:
            deps += gen_expr_deps(unit, statement.each_clause)

        if statement.while_clause is not None:
            deps += gen_expr_deps(unit, statement.while_clause)

        if statement.loop_body is not None:
            deps += gen_block_deps(unit, statement.loop_body)

        if statement.then_clause is not None:
            deps += gen_expr_deps(unit, statement.then_clause)

        if statement.until_clause is not None:
            deps += gen_expr_deps(unit, statement.until_clause)

    return deps

def gen_switch_deps(unit, statement):
    assert statement.scope is not None

    deps = [ ]

    with unit.use_scope(statement.scope):
        for case_values, case_block in statement.case_branches:
            for value in case_values:
                deps += gen_expr_deps(unit, value)
            deps += gen_block_deps(unit, case_block)

        if statement.default_block is not None:
            deps += gen_block_deps(unit, statement.default_block)

    return deps

def gen_try_deps(unit, statement):
    deps = gen_block_deps(unit, statement.try_block)

    for clause in statement.catch_clauses:
        assert clause.scope is not None

        with unit.use_scope(clause.scope):
            deps += gen_expr_deps(unit, clause.type)
            deps += gen_block_deps(unit, clause.block)

    if statement.default_catch is not None:
        deps += gen_block_deps(unit, statement.default_catch)

    return deps
