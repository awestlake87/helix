from contextlib import contextmanager

from .lexer import scan_tokens
from .token import Token

from .exprs import *
from .statements import *
from .types import *
from .values import *
from .condition_nodes import *

from ..err import Todo, ExpectedToken, UnexpectedToken, CompilerBug

def parse_unit(unit_id, unit_code):
    class Context:
        def __init__(self, code):
            self.scanner = scan_tokens(code)
            self._scan_queue = [
                Token(Token.NONE),
                next(self.scanner)
            ]

            self._use_prescanner = False
            self._prescan_cursor = 0

        @property
        def current(self):
            if self._use_prescanner:
                assert self._prescan_cursor < len(self._scan_queue)

                return self._scan_queue[self._prescan_cursor]

            else:
                assert len(self._scan_queue) > 0

                return self._scan_queue[0]

        @current.setter
        def current(self, token):
            if self._use_prescanner:
                assert self._prescan_cursor < len(self._scan_queue)

                self._scan_queue[self._prescan_cursor] = token

            else:
                assert len(self._scan_queue) > 0

                self._scan_queue[0] = token

        @property
        def next(self):
            if self._use_prescanner:
                assert self._prescan_cursor + 1 < len(self._scan_queue)

                return self._scan_queue[self._prescan_cursor + 1]

            else:
                assert len(self._scan_queue) > 1

                return self._scan_queue[1]

        def peek(self):
            return self.next.id

        def accept(self, id):
            if self._use_prescanner:
                if self.peek() == id:
                    while self._prescan_cursor + 2 >= len(self._scan_queue):
                        self._scan_queue.append(next(self.scanner))

                    self._prescan_cursor += 1

                    return True

                else:
                    return False

            else:
                if self.peek() == id:
                    self._scan_queue.pop(0)
                    self._scan_queue.append(next(self.scanner))

                    return True

                else:
                    return False

        def expect(self, id):
            if not self.accept(id):
                raise ExpectedToken(Token(id), self.next)

        @contextmanager
        def use_prescanner(self):
            old_cursor = self._prescan_cursor
            old_use_prescanner = self._use_prescanner

            self._prescan_cursor = 0
            self._use_prescanner = True

            yield

            self._prescan_cursor = old_cursor
            self._use_prescanner = old_use_prescanner


    ctx = Context(unit_code)

    block = parse_block(ctx)
    ctx.expect(Token.END)

    return UnitNode(unit_id, block)

def parse_block(ctx):
    ctx.accept(Token.KW_DO)
    ctx.expect(Token.INDENT)

    if ctx.accept(Token.KW_PASS):
        ctx.accept(Token.NODENT)
        ctx.expect(Token.DEDENT)

        return BlockNode([ ])

    else:
        statements = [ ]

        while not ctx.accept(Token.DEDENT):
            statements.append(parse_statement(ctx))
            ctx.accept(Token.NODENT)

        return BlockNode(statements)

def parse_statement(ctx):
    id = ctx.peek()

    if id == Token.KW_RETURN:
        return parse_return(ctx)

    elif id == Token.KW_SWITCH:
        return parse_switch(ctx)

    elif id == Token.KW_IF:
        return parse_if(ctx)

    elif id == Token.KW_DO:
        return parse_block(ctx)

    elif (
        id == Token.KW_FOR or
        id == Token.KW_WHILE or
        id == Token.KW_EACH or
        id == Token.KW_LOOP
    ):
        return parse_loop(ctx)

    elif id == Token.KW_TRY:
        return parse_try(ctx)

    elif ctx.accept(Token.KW_THROW):
        return ThrowNode(parse_expr(ctx))

    elif ctx.accept(Token.KW_BREAK):
        return BreakNode()

    elif ctx.accept(Token.KW_CONTINUE):
        return ContinueNode()

    else:
        return parse_expr(ctx)

def parse_loop(ctx):
    for_clause = None
    each_clause = None
    while_clause = None

    loop_kw_required = True

    if ctx.accept(Token.KW_FOR):
        for_clause = parse_expr(ctx)
        loop_kw_required = False

    if ctx.accept(Token.KW_WHILE):
        while_clause = parse_expr(ctx)
        loop_kw_required = False

    if loop_kw_required:
        ctx.expect(Token.KW_LOOP)
    else:
        ctx.accept(Token.KW_LOOP)

    loop_body = parse_block(ctx)

    then_clause = None
    until_clause = None

    parse_then = False
    parse_until = False

    with ctx.use_prescanner():
        if ctx.accept(Token.NODENT):
            if ctx.accept(Token.KW_THEN):
                parse_then = True

            if ctx.accept(Token.KW_UNTIL):
                parse_until = True

    if parse_then:
        ctx.expect(Token.NODENT)
        ctx.expect(Token.KW_THEN)
        then_clause = parse_expr(ctx)

    if parse_until:
        ctx.expect(Token.NODENT)
        ctx.expect(Token.KW_UNTIL)
        until_clause = parse_expr(ctx)

    return LoopNode(
        for_clause,
        each_clause,
        while_clause,
        loop_body,
        then_clause,
        until_clause
    )

def parse_switch(ctx):
    ctx.expect(Token.KW_SWITCH)

    value = parse_expr(ctx)

    ctx.expect(Token.INDENT)

    if ctx.accept(Token.KW_PASS):
        ctx.accept(Token.NODENT)
        ctx.expect(Token.DEDENT)
        return SwitchStatement(value)
    else:
        case_branches = [ ]
        default_block = None

        while ctx.accept(Token.KW_CASE):
            case_values = [ parse_expr(ctx) ]

            while ctx.accept(Token.NODENT):
                ctx.expect(Token.KW_CASE)
                case_values.append(parse_expr(ctx))

            case_block = parse_block(ctx)

            switch_continues = False

            with ctx.use_prescanner():
                if ctx.accept(Token.NODENT):
                    if (
                        ctx.accept(Token.KW_CASE) or
                        ctx.accept(Token.KW_DEFAULT)
                    ):
                        switch_continues = True

            if switch_continues:
                ctx.expect(Token.NODENT)

            case_branches.append((case_values, case_block))

        if ctx.accept(Token.KW_DEFAULT):
            default_block = parse_block(ctx)

        ctx.expect(Token.DEDENT)
        return SwitchNode(value, case_branches, default_block)

def parse_if(ctx):
    ctx.expect(Token.KW_IF)

    if_cond = parse_expr(ctx)
    if_block = parse_block(ctx)

    ctx.accept(Token.NODENT)

    if_branches = [ ]

    if_branches.append((if_cond, if_block))

    while ctx.accept(Token.KW_ELIF):
        cond = parse_expr(ctx)
        block = parse_block(ctx)

        if_continues = False

        with ctx.use_prescanner():
            if ctx.accept(Token.NODENT):
                if ctx.accept(Token.KW_ELIF) or ctx.accept(Token.KW_ELSE):
                    if_continues = True

        if if_continues:
            ctx.expect(Token.NODENT)

        if_branches.append((cond, block))

    if ctx.accept(Token.KW_ELSE):
        return IfNode(if_branches, parse_block(ctx))

    else:
        return IfNode(if_branches)

def parse_try(ctx):
    ctx.expect(Token.KW_TRY)

    try_block = parse_block(ctx)

    catch_clauses = [ ]
    default_catch = None

    ctx.expect(Token.NODENT)

    while ctx.accept(Token.KW_CATCH):
        if ctx.peek() == Token.INDENT:
            default_catch = parse_block(ctx)
            break

        else:
            type_expr = parse_expr(ctx)
            ctx.expect(Token.ID)
            id = ctx.current.value
            block = parse_block(ctx)

            catch_clauses.append(CatchNode(type_expr, id, block))

        try_continues = False
        with ctx.use_prescanner():
            if ctx.accept(Token.NODENT):
                if ctx.accept(Token.KW_CATCH):
                    try_continues = True

        if try_continues:
            ctx.expect(Token.NODENT)

    if len(catch_clauses) == 0 and default_catch is None:
        raise Todo("try must have at least one catch")

    return TryNode(try_block, catch_clauses, default_catch)


def parse_expr(ctx):
    return parse_expr_prec20(ctx)

def parse_expr_prec20(ctx):
    lhs = parse_expr_prec19(ctx)

    while ctx.accept(Token.OP_OR):
        lhs = OrNode(lhs, parse_expr_prec19(ctx))

    return lhs

def parse_expr_prec19(ctx):
    lhs = parse_expr_prec18(ctx)

    while ctx.accept(Token.OP_XOR):
        lhs = XorNode(lhs, parse_expr_prec18(ctx))

    return lhs

def parse_expr_prec18(ctx):
    lhs = parse_expr_prec17(ctx)

    while ctx.accept(Token.OP_AND):
        lhs = AndNode(lhs, parse_expr_prec17(ctx))

    return lhs

def parse_expr_prec17(ctx):
    def accept_op():
        if ctx.accept(Token.OP_EQ) or ctx.accept(Token.OP_NEQ):
            return True
        else:
            return False

    lhs = parse_expr_prec16(ctx)

    while accept_op():
        id = ctx.current.id

        if id == Token.OP_EQ:
            lhs = EqlNode(lhs, parse_expr_prec16(ctx))
        elif id == Token.OP_NEQ:
            lhs = NeqNode(lhs, parse_expr_prec16(ctx))
        else:
            raise CompilerBug("~.~")

    return lhs

def parse_expr_prec16(ctx):
    def accept_op():
        if ctx.accept('<') or ctx.accept('>'):
            return True
        elif ctx.accept(Token.OP_LEQ) or ctx.accept(Token.OP_GEQ):
            return True
        else:
            return False

    lhs = parse_expr_prec15(ctx)

    while accept_op():
        id = ctx.current.id

        if id == '<':
            lhs = LtnNode(lhs, parse_expr_prec15(ctx))
        elif id == '>':
            lhs = GtnNode(lhs, parse_expr_prec15(ctx))
        elif id == Token.OP_LEQ:
            lhs = LeqNode(lhs, parse_expr_prec15(ctx))
        elif id == Token.OP_GEQ:
            lhs = GeqNode(lhs, parse_expr_prec15(ctx))
        else:
            raise CompilerBug("8.8")

    return lhs

def parse_expr_prec15(ctx):
    if ctx.accept(Token.OP_NOT):
        id = ctx.current.id

        if id == Token.OP_NOT:
            return NotNode(parse_expr_prec15(ctx))
        else:
            raise CompilerBug("%.%")
    else:
        return parse_expr_prec14(ctx)

def parse_expr_prec14(ctx):
    lhs = parse_expr_prec13(ctx)

    if ctx.accept(':'):
        return InitNode(lhs, parse_expr_prec14(ctx))
    elif ctx.accept('='):
        return AssignNode(lhs, parse_expr_prec14(ctx))

    elif ctx.accept(Token.OP_ADD_ASSIGN):
        return AssignNode(lhs, AddNode(lhs, parse_expr_prec14(ctx)))

    elif ctx.accept(Token.OP_SUB_ASSIGN):
        return AssignNode(lhs, SubNode(lhs, parse_expr_prec14(ctx)))
    elif ctx.accept(Token.OP_MUL_ASSIGN):
        return AssignNode(lhs, MulNode(lhs, parse_expr_prec14(ctx)))
    elif ctx.accept(Token.OP_DIV_ASSIGN):
        return AssignNode(lhs, DivNode(lhs, parse_expr_prec14(ctx)))
    elif ctx.accept(Token.OP_MOD_ASSIGN):
        return AssignNode(lhs, ModNode(lhs, parse_expr_prec14(ctx)))

    elif ctx.accept(Token.OP_AND_ASSIGN):
        return AssignNode(lhs, BitAndNode(lhs, parse_expr_prec14(ctx)))
    elif ctx.accept(Token.OP_XOR_ASSIGN):
        return AssignNode(lhs, BitXorNode(lhs, parse_expr_prec14(ctx)))
    elif ctx.accept(Token.OP_OR_ASSIGN):
        return AssignNode(lhs, BitOrNode(lhs, parse_expr_prec14(ctx)))
    elif ctx.accept(Token.OP_SHL_ASSIGN):
        return AssignNode(lhs, BitShlNode(lhs, parse_expr_prec14(ctx)))
    elif ctx.accept(Token.OP_SHR_ASSIGN):
        return AssignNode(lhs, BitShrNode(lhs, parse_expr_prec14(ctx)))

    else:
        return lhs

def parse_expr_prec13(ctx):
    lhs = parse_expr_prec12(ctx)

    if ctx.accept(Token.KW_IF):
        condition = parse_expr(ctx)

        ctx.expect(Token.KW_ELSE)

        rhs = parse_expr_prec12(ctx)

        return TernaryConditionalNode(lhs, condition, rhs)

    else:
        return lhs

def parse_expr_prec12(ctx):
    lhs = parse_expr_prec11(ctx)

    while ctx.accept('|'):
        lhs = BitOrNode(lhs, parse_expr_prec11(ctx))

    return lhs

def parse_expr_prec11(ctx):
    lhs = parse_expr_prec10(ctx)

    while ctx.accept('^'):
        lhs = BitXorNode(lhs, parse_expr_prec10(ctx))

    return lhs

def parse_expr_prec10(ctx):
    lhs = parse_expr_prec9(ctx)

    while ctx.accept('&'):
        lhs = BitAndNode(lhs, parse_expr_prec9(ctx))

    return lhs

def parse_expr_prec9(ctx):
    def accept_op():
        if ctx.accept(Token.OP_SHL) or ctx.accept(Token.OP_SHR):
            return True
        else:
            return False

    lhs = parse_expr_prec8(ctx)

    while accept_op():
        id = ctx.current.id

        if id == Token.OP_SHL:
            lhs = BitShlNode(lhs, parse_expr_prec8(ctx))
        elif id == Token.OP_SHR:
            lhs = BitShrNode(lhs, parse_expr_prec8(ctx))
        else:
            raise CompilerBug("^.^")

    return lhs

def parse_expr_prec8(ctx):
    def accept_op():
        if ctx.accept('+') or ctx.accept('-'):
            return True
        else:
            return False

    lhs = parse_expr_prec7(ctx)

    while accept_op():
        id = ctx.current.id

        if id == '+':
            lhs = AddNode(lhs, parse_expr_prec7(ctx))
        elif id == '-':
            lhs = SubNode(lhs, parse_expr_prec7(ctx))
        else:
            raise CompilerBug("*_*")

    return lhs

def parse_expr_prec7(ctx):
    def accept_op():
        if ctx.accept('*') or ctx.accept('/') or ctx.accept('%'):
            return True
        else:
            return False

    lhs = parse_expr_prec6(ctx)

    while accept_op():
        id = ctx.current.id

        if id == '*':
            lhs = MulNode(lhs, parse_expr_prec6(ctx))
        elif id == '/':
            lhs = DivNode(lhs, parse_expr_prec6(ctx))
        elif id == '%':
            lhs = ModNode(lhs, parse_expr_prec6(ctx))
        else:
            raise CompilerBug("$_$")

    return lhs

def parse_expr_prec6(ctx):
    def accept_op():
        if ctx.accept(Token.OP_AS):
            return True
        elif ctx.accept(Token.OP_CAST):
            return True
        elif ctx.accept(Token.OP_BITCAST):
            return True
        elif ctx.accept(Token.OP_OFFSETOF):
            return True
        else:
            return False

    lhs = parse_expr_prec5(ctx)

    while accept_op():
        id = ctx.current.id

        if id == Token.OP_AS:
            lhs = AsNode(lhs, parse_expr_prec5(ctx))
        elif id == Token.OP_CAST:
            lhs = CastNode(lhs, parse_expr_prec5(ctx))
        elif id == Token.OP_BITCAST:
            lhs = BitcastNode(lhs, parse_expr_prec5(ctx))

        elif id == Token.OP_OFFSETOF:
            lhs = OffsetofNode(lhs, parse_expr_prec5(ctx))

        else:
            raise CompilerBug("$_#")

    return lhs

def parse_expr_prec5(ctx):
    if ctx.accept(Token.OP_SIZEOF):
        return SizeofNode(parse_expr_prec5(ctx))

    else:
        return parse_expr_prec4(ctx)

def parse_expr_prec4(ctx):
    def is_embed_call():
        # TODO: MAKE THIS BETTER
        # look ahead to determine whether it's a condition or
        # embed call

        with ctx.use_prescanner():
            ctx.expect('<')

            if ctx.accept('>'):
                # replace right bracket with token denoting embed call
                ctx.current = Token(Token.OP_R_EMBED)
                return True

            elif ctx.accept(Token.LT_INT_DEC):
                if ctx.accept('>'):
                    # replace right bracket with token denoting embed call
                    ctx.current = Token(Token.OP_R_EMBED)
                    return True

                else:
                    return False

            else:
                return False

    def accept_op():
        if ctx.accept('('):
            return True

        elif ctx.accept('['):
            return True

        elif ctx.peek() == '<':
            if is_embed_call():
                ctx.expect('<')
                # replace left bracket with token denoting embed call
                ctx.current = Token(Token.OP_L_EMBED)
                return True

            else:
                return False

        elif ctx.accept('!'):
            return True

        elif ctx.accept('~'):
            return True

        elif ctx.accept(Token.OP_INC):
            return True

        elif ctx.accept(Token.OP_DEC):
            return True

        else:
            return False

    lhs = parse_expr_prec3(ctx)

    while accept_op():
        id = ctx.current.id

        if id == '(':
            args = [ ]

            if not ctx.accept(')'):
                while True:
                    args.append(parse_expr(ctx))
                    if not ctx.accept(','):
                        ctx.expect(')')
                        break

            lhs = CallNode(lhs, args)

        elif id == '[':
            expr = parse_expr(ctx)

            ctx.expect(']')

            lhs = IndexNode(lhs, expr)

        elif id == Token.OP_L_EMBED:
            args = [ ]

            if not ctx.accept(Token.OP_R_EMBED):
                while True:
                    args.append(parse_expr(ctx))
                    if not ctx.accept(','):
                        ctx.expect(Token.OP_R_EMBED)
                        break

            lhs = EmbedCallNode(lhs, args)

        elif id == '!':
            lhs = BangNode(lhs)

        elif id == "~":
            lhs = TropeNode(lhs)

        elif id == Token.OP_INC:
            lhs = PostIncNode(lhs)

        elif id == Token.OP_DEC:
            lhs = PostDecNode(lhs)

        else:
            raise CompilerBug("O_o")

    return lhs

def parse_expr_prec3(ctx):
    if ctx.accept('*'):
        return PtrNode(parse_expr_prec3(ctx))

    elif ctx.accept('&'):
        return RefNode(parse_expr_prec3(ctx))

    elif ctx.accept(Token.KW_MUT):
        return MutNode(parse_expr_prec3(ctx))

    elif ctx.accept('-'):
        return NegNode(parse_expr_prec3(ctx))

    elif ctx.accept(Token.OP_INC):
        return PreIncNode(parse_expr_prec3(ctx))

    elif ctx.accept(Token.OP_DEC):
        return PreDecNode(parse_expr_prec3(ctx))

    elif ctx.accept('~'):
        return BitNotNode(parse_expr_prec3(ctx))

    elif ctx.accept('['):
        length = parse_expr(ctx)
        ctx.expect(']')
        return ArrayTypeNode(length, parse_expr_prec3(ctx))

    else:
        return parse_expr_prec2(ctx)

def parse_expr_prec2(ctx):
    def accept_op():
        if ctx.accept('.'):
            return True
        else:
            return False

    lhs = parse_expr_prec1(ctx)

    while accept_op():
        id = ctx.current.id

        if id == '.':
            lhs = DotNode(lhs, parse_expr_prec1(ctx))
        else:
            raise CompilerBug("%.%")

    return lhs

def parse_expr_prec1(ctx):
    if ctx.accept(Token.ID):
        return SymbolNode(ctx.current.value)

    elif ctx.accept('('):
        expr = parse_expr(ctx)
        ctx.expect(')')
        return expr

    elif ctx.accept(Token.LT_INT_DEC):
        return AutoIntNode(ctx.current.value, radix=10)

    elif ctx.accept(Token.LT_INT_BIN):
        return AutoIntNode(ctx.current.value, radix=2)

    elif ctx.accept(Token.LT_TRUE):
        return IntNode(1, False, 1)

    elif ctx.accept(Token.LT_FALSE):
        return IntNode(1, False, 0)

    elif ctx.accept(Token.LT_NIL):
        return NilNode()

    elif ctx.accept(Token.LT_STRING):
        return StringNode(ctx.current.value)

    elif ctx.accept(Token.LT_CHAR):
        return IntNode(8, False, ord(ctx.current.value))

    elif ctx.accept(Token.KW_BIT):
        return IntTypeNode(1, False)

    elif ctx.accept(Token.KW_CHAR):
        return IntTypeNode(8, False)

    elif ctx.accept(Token.KW_BYTE):
        return IntTypeNode(8, True)

    elif ctx.accept(Token.KW_SHORT):
        return IntTypeNode(16, True)

    elif ctx.accept(Token.KW_INT):
        return IntTypeNode(32, True)

    elif ctx.accept(Token.KW_LONG):
        return IntTypeNode(64, True)

    elif ctx.accept(Token.KW_UBYTE):
        return IntTypeNode(8, False)

    elif ctx.accept(Token.KW_USHORT):
        return IntTypeNode(16, False)

    elif ctx.accept(Token.KW_UINT):
        return IntTypeNode(32, False)

    elif ctx.accept(Token.KW_ULONG):
        return IntTypeNode(64, False)

    elif ctx.accept(Token.KW_VOID):
        return VoidTypeNode()

    elif ctx.accept(Token.KW_AUTO):
        return AutoTypeNode()

    elif ctx.accept('@'):
        ctx.expect(Token.ID)
        return AttrNode(ctx.current.value)

    else:
        if ctx.peek() == Token.KW_STRUCT:
            return parse_struct(ctx)

        elif ctx.peek() == Token.KW_FUN or ctx.peek() == Token.KW_CFUN:
            return parse_fun(ctx)

        elif ctx.peek() == Token.KW_OPER:
            return parse_oper(ctx)

        elif ctx.peek() == Token.KW_CGLOBAL or ctx.peek() == Token.KW_GLOBAL:
            return parse_global(ctx)

        else:
            raise UnexpectedToken(ctx.next)


def parse_fun(ctx):
    is_cfun = False
    is_vargs = False
    is_attr = False
    is_mut = False
    param_types = [ ]
    param_ids = [ ]

    if ctx.accept(Token.KW_CFUN):
        is_cfun = True

    else:
        ctx.expect(Token.KW_FUN)

    ret_type = parse_expr(ctx)

    if ctx.accept('@'):
        is_attr = True

        if ctx.accept(Token.KW_MUT):
            is_mut = True

    ctx.expect(Token.ID)

    id = ctx.current.value

    ctx.expect('(')

    if not ctx.accept(')'):
        while True:
            if ctx.accept(Token.KW_VARGS):
                is_vargs = True
                break

            else:
                param_types.append(parse_expr(ctx))

                ctx.expect(Token.ID)

                param_ids.append(ctx.current.value)

                if not ctx.accept(','):
                    break

        ctx.expect(')')

    block = None

    if ctx.peek() == Token.INDENT:
        block = parse_block(ctx)

    return FunNode(
        FunTypeNode(ret_type, param_types),
        id,
        param_ids,
        block,
        is_cfun = is_cfun,
        is_vargs = is_vargs,
        is_attr = is_attr,
        is_mut = is_mut
    )

def parse_oper(ctx):
    def parse_params():
        param_types = [ ]
        param_ids = [ ]

        ctx.expect('(')

        if not ctx.accept(')'):
            while True:
                param_types.append(parse_expr(ctx))

                ctx.expect(Token.ID)

                param_ids.append(ctx.current.value)

                if not ctx.accept(','):
                    break

            ctx.expect(')')

        return (param_types, param_ids)

    ctx.expect(Token.KW_OPER)

    if ctx.accept(Token.OP_CONSTRUCT):
        param_types, param_ids = parse_params()
        block = parse_block(ctx)

        return ConstructOperNode(param_types, param_ids, block)

    elif ctx.accept(Token.OP_DESTRUCT):
        ctx.expect('(')
        ctx.expect(')')
        block = parse_block(ctx)

        return DestructOperNode(block)

    else:
        raise Todo()

def parse_struct(ctx):
    ctx.expect(Token.KW_STRUCT)

    ctx.expect(Token.ID)
    id = ctx.current.value

    ctx.expect(Token.INDENT)

    if ctx.accept(Token.KW_PASS):
        ctx.expect(Token.DEDENT)
        return StructNode(id)

    else:
        attrs = [ ]

        while not ctx.accept(Token.DEDENT):
            if (
                ctx.peek() == Token.KW_FUN or
                ctx.peek() == Token.KW_CFUN
            ):
                fun = parse_fun(ctx)

                attrs.append((fun.id, fun))

            elif ctx.peek() == Token.KW_OPER:
                oper = parse_oper(ctx)

                attrs.append((oper.id, oper))

            else:
                attr_type = parse_expr(ctx)

                ctx.expect('@')
                ctx.expect(Token.ID)
                attr_id = ctx.current.value

                if attr_id and attr_id not in attrs:
                    attrs.append((attr_id, DataAttr(attr_type, attr_id)))

            ctx.accept(Token.NODENT)

        return StructNode(id, attrs)

def parse_global(ctx):
    is_cglobal = False

    if ctx.accept(Token.KW_CGLOBAL):
        is_cglobal = True

    else:
        ctx.expect(Token.KW_GLOBAL)

    expr = parse_expr(ctx)

    if ctx.accept(Token.ID):
        id = ctx.current.value
        return GlobalNode(expr, id, is_cglobal=is_cglobal)

    elif type(expr) is InitNode:
        if type(expr.lhs) is SymbolNode:
            id = expr.lhs.id
            return InitNode(
                GlobalNode(AutoTypeNode(), id, is_cglobal=is_cglobal),
                expr.rhs
            )
        else:
            raise Todo(expr.lhs)

    else:
        raise Todo(expr)

def parse_return(ctx):
    ctx.expect(Token.KW_RETURN)

    if ctx.peek() != Token.NODENT and ctx.peek() != Token.DEDENT:
        return ReturnNode(parse_expr(ctx))

    else:
        return ReturnNode()
