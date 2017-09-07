
from ..ast import *
from ..err import *
from ..sym import *

def gen_expr_sym(unit, expr):
    expr_type = type(expr)

    if expr_type is SymbolNode:
        return unit.scope.resolve(expr.id)

    elif expr_type is GlobalNode:
        return unit.scope.resolve(expr.id)

    elif expr_type is DotNode:
        lhs = gen_expr_sym(unit, expr.lhs)

        if type(lhs) is VarSymbol or type(lhs) is GlobalSymbol:
            if type(lhs.type) is StructSymbol:
                if type(expr.rhs) is SymbolNode:
                    sym = lhs.type.get_attr_symbol(expr.rhs.id)

                    if type(sym) is StructSymbol:
                        return VarSymbol(sym)

                    else:
                        return sym

                else:
                    raise Todo()

    elif expr_type is CallNode:
        lhs = gen_expr_sym(unit, expr.lhs)

        if type(lhs) is StructSymbol:
            return VarSymbol(lhs)

        else:
            return None

    else:
        return None


def gen_unit_deps(unit):
    jit_fun = FunSymbol(
        unit,
        FunNode(
            FunTypeNode(BangNode(IntTypeNode(32, True)), [ ]),
            OperName(OperName.OP_JIT),
            [ ],
            unit.ast.block
        ),
        unit.scope
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

    if statement_type is ReturnNode:
        return gen_return_deps(unit, statement)

    elif statement_type is IfNode:
        return gen_if_statement_deps(unit, statement)

    elif statement_type is LoopNode:
        return gen_loop_statement_deps(unit, statement)

    elif statement_type is SwitchNode:
        return gen_switch_statement_deps(unit, statement)

    elif statement_type is TryNode:
        return gen_try_statement_deps(unit, statement)

    elif statement_type is ThrowStatementNode:
        return gen_expr_deps(unit, statement.expr)

    elif statement_type is BreakNode or statement_type is ContinueNode:
        return [ ]

    elif issubclass(statement_type, ExprNode):
        return gen_expr_deps(unit, statement)

    elif statement_type is BlockNode:
        return gen_block_deps(unit, statement)

    else:
        raise Todo(repr(statement))

def gen_expr_deps(unit, expr):
    expr_type = type(expr)

    if expr_type is CallNode:
        return gen_call_deps(unit, expr)

    elif expr_type is EmbedCallNode:
        return gen_call_deps(unit, expr)

    elif expr_type is DotNode:
        return gen_dot_expr_deps(unit, expr)

    elif expr_type is InitNode:
        return gen_init_expr_deps(unit, expr)

    elif expr_type is TernaryConditionalNode:
        return gen_ternary_conditional_deps(unit, expr)

    elif issubclass(expr_type, UnaryExprNode):
        return gen_unary_expr_deps(unit, expr)

    elif issubclass(expr_type, BinaryExprNode):
        return gen_binary_expr_deps(unit, expr)

    elif expr_type is StructNode:
        return gen_struct_deps(unit, expr)

    elif expr_type is FunNode:
        return gen_fun_deps(unit, unit.scope.resolve(expr.id))

    elif expr_type is SymbolNode:
        sym = unit.scope.resolve(expr.id)

        if type(sym) is FunSymbol:
            return [ sym.proto_target ]

        else:
            return [ sym.target ]

    elif expr_type is FunTypeNode:
        return gen_fun_type_deps(unit, expr)

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
            gen_expr_deps(unit, expr.length) +
            gen_expr_deps(unit, expr.type)
        )

    elif expr_type is GlobalNode:
        return gen_global_deps(unit, expr)

    elif issubclass(expr_type, LiteralNode):
        return [ ]

    else:
        raise Todo(expr)

def gen_struct_deps(unit, expr):
    symbol = unit.scope.resolve(expr.id)

    for attr_id, attr_symbol in symbol.attrs:
        attr_type = type(attr_symbol)

        if attr_type is DataAttrSymbol:
            symbol.target.deps += gen_expr_deps(
                unit, attr_symbol.ast.type
            )
            symbol.target.attrs[attr_id] = attr_symbol

        elif issubclass(attr_type, AttrFunSymbol):
            symbol.target.attrs[attr_id] = attr_symbol

        else:
            raise Todo()

    return [ ]

def gen_fun_deps(unit, symbol):
    symbol.proto_target.deps += gen_expr_deps(unit, symbol.ast.type)

    if symbol.ast.body is not None:
        with unit.use_scope(symbol.scope):
            symbol.target.deps += gen_block_deps(unit, symbol.ast.body)

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

    if type(lhs) is GlobalSymbol:
        deps.append(lhs.target)

    sym = gen_expr_sym(unit, expr)

    if type(sym) is AttrFunSymbol:
        deps.append(sym.target)

    elif type(sym) is GlobalSymbol:
        deps.append(sym.target)

    return deps

def gen_init_expr_deps(unit, expr):
    deps = gen_expr_deps(unit, expr.lhs) + gen_expr_deps(unit, expr.rhs)

    lhs = gen_expr_sym(unit, expr.lhs)
    rhs = gen_expr_sym(unit, expr.rhs)

    if type(rhs) is VarSymbol:
        lhs.type = rhs.type

    elif type(rhs) is GlobalSymbol:
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

    if type(lhs) is StructSymbol:
        ctor = lhs.get_ctor_symbol()
        dtor = lhs.get_dtor_symbol()

        if ctor is not None:
            deps.append(ctor.target)

        if dtor is not None:
            deps.append(dtor.target)

    elif type(lhs) is FunSymbol or type(lhs) is AttrFunSymbol:
        if lhs.target is not None:
            unit.target.deps.append(lhs.target)

    return deps

def gen_fun_type_deps(unit, fun_type):
    deps = gen_expr_deps(unit, fun_type.ret_type)

    for param in fun_type.param_types:
        if type(param) is BangNode:
            deps += gen_expr_deps(unit, param.operand)

        else:
            raise Todo()

    return deps

def gen_return_deps(unit, statement):
    if statement.expr is not None:
        return gen_expr_deps(unit, statement.expr)

    else:
        return [ ]

def gen_if_statement_deps(unit, statement):
    assert statement.scope is not None

    deps = [ ]

    with unit.use_scope(statement.scope):
        for condition, block in statement.if_branches:
            deps += gen_expr_deps(unit, condition)
            deps += gen_block_deps(unit, block)

        if statement.else_block is not None:
            deps += gen_block_deps(unit, statement.else_block)

    return deps

def gen_loop_statement_deps(unit, statement):
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

def gen_switch_statement_deps(unit, statement):
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

def gen_try_statement_deps(unit, statement):
    deps = gen_block_deps(unit, statement.try_block)

    for clause in statement.catch_clauses:
        assert clause.scope is not None

        with unit.use_scope(clause.scope):
            deps += gen_expr_deps(unit, clause.type)
            deps += gen_block_deps(unit, clause.block)

    if statement.default_catch is not None:
        deps += gen_block_deps(unit, statement.default_catch)

    return deps
