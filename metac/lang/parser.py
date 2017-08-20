from .lexer import Lexer
from .token import Token

from ..ast import *
from ..err import Todo, ExpectedToken, UnexpectedToken, CompilerBug

class Parser:
    def __init__(self, str):
        self._lexer = Lexer(str)
        self._current = Token(Token.NONE)
        self._next = self._lexer.scan()
        self._ahead = self._lexer.scan()

    def parse(self):
        block = self._parse_block()

        self._expect(Token.END)

        return block

    def _peek_ahead(self):
        return self._ahead.id

    def _peek(self):
        return self._next.id

    def _expect(self, id):
        if not self._accept(id):
            raise ExpectedToken(Token(id), self._next)

    def _accept(self, id):
        if self._peek() == id:
            self._current = self._next
            self._next = self._ahead
            self._ahead = self._lexer.scan()
            return True
        else:
            return False

    def _parse_block(self):
        self._accept(Token.KW_DO)
        self._expect(Token.INDENT)

        if self._accept(Token.KW_PASS):
            self._accept(Token.NODENT)
            self._expect(Token.DEDENT)

            return BlockNode([ ])

        else:
            statements = [ ]

            while not self._accept(Token.DEDENT):
                statements.append(self._parse_statement())
                self._accept(Token.NODENT)

            return BlockNode(statements)

    def _parse_statement(self):
        id = self._peek()

        if id == Token.KW_RETURN:
            return self._parse_return_statement()

        elif id == Token.KW_SWITCH:
            return self._parse_switch_statement()

        elif id == Token.KW_IF:
            return self._parse_if_statement()

        elif id == Token.KW_DO:
            return self._parse_block()

        elif id == Token.KW_FOR:
            return self._parse_loop()

        elif id == Token.KW_WHILE:
            return self._parse_loop()

        elif id == Token.KW_EACH:
            return self._parse_loop()

        elif id == Token.KW_LOOP:
            return self._parse_loop()

        elif self._accept(Token.KW_BREAK):
            return BreakNode()

        elif self._accept(Token.KW_CONTINUE):
            return ContinueNode()

        else:
            return self._parse_expr()

    def _parse_return_statement(self):
        self._expect(Token.KW_RETURN)

        return ReturnNode(self._parse_expr())

    def _parse_switch_statement(self):
        self._expect(Token.KW_SWITCH)

        value = self._parse_expr()

        self._expect(Token.INDENT)

        if self._accept(Token.KW_PASS):
            self._accept(Token.NODENT)
            self._expect(Token.DEDENT)
            return SwitchStatement(value)
        else:
            case_branches = [ ]
            default_block = None

            while self._accept(Token.KW_CASE):
                case_values = [ self._parse_expr() ]

                while self._accept(Token.NODENT):
                    self._expect(Token.KW_CASE)
                    case_values.append(self._parse_expr())

                case_block = self._parse_block()

                if (
                    self._peek_ahead() == Token.KW_CASE or
                    self._peek_ahead() == Token.KW_DEFAULT
                ):
                    self._accept(Token.NODENT)

                case_branches.append((case_values, case_block))

            if self._accept(Token.KW_DEFAULT):
                default_block = self._parse_block()

            self._expect(Token.DEDENT)
            return SwitchStatementNode(value, case_branches, default_block)

    def _parse_if_statement(self):
        self._expect(Token.KW_IF)

        if_cond = self._parse_condition()
        if_block = self._parse_block()

        self._accept(Token.NODENT)

        if_branches = [ ]

        if_branches.append((if_cond, if_block))

        while self._accept(Token.KW_ELIF):
            cond = self._parse_condition()
            block = self._parse_block()

            if (
                self._peek_ahead() == Token.KW_ELIF or
                self._peek_ahead() == Token.KW_ELSE
            ):
                self._accept(Token.NODENT)

            if_branches.append((cond, block))

        if self._accept(Token.KW_ELSE):
            return IfStatementNode(if_branches, self._parse_block())

        else:
            return IfStatementNode(if_branches)


    def _parse_fun(self):
        self._expect(Token.KW_EXTERN)
        self._expect(Token.KW_FUN)

        ret_type = self._parse_expr()

        self._expect(Token.ID)
        id = self._current.value

        self._expect('(')

        param_types = [ ]
        param_ids = [ ]

        if not self._accept(')'):
            while True:
                param_types.append(self._parse_expr())

                self._expect(Token.ID)

                param_ids.append(self._current.value)

                if not self._accept(','):
                    break

            self._expect(')')

        if self._peek() == Token.INDENT:
            return FunNode(
                FunTypeNode(ret_type, param_types),
                id,
                param_ids,
                self._parse_block()
            )
        else:
            return FunNode(
                FunTypeNode(ret_type, param_types),
                id,
                param_ids,
                None
            )

    def _parse_struct(self):
        self._expect(Token.KW_STRUCT)

        self._expect(Token.ID)
        id = self._current.value

        self._expect(Token.INDENT)

        if self._accept(Token.KW_PASS):
            self._expect(Token.DEDENT)
            return StructNode(id)

        else:
            attrs = [ ]

            while not self._accept(Token.DEDENT):
                attr_type = self._parse_expr()

                self._expect(Token.ATTR_ID)
                attr_id = self._current.value

                attrs.append((attr_type, attr_id))

                self._accept(Token.NODENT)

            return StructNode(id, attrs)

    def _parse_loop(self):
        for_clause = None
        each_clause = None
        while_clause = None

        loop_kw_required = True

        if self._accept(Token.KW_FOR):
            for_clause = self._parse_expr()
            loop_kw_required = False

        if self._accept(Token.KW_WHILE):
            while_clause = self._parse_condition()
            loop_kw_required = False

        if loop_kw_required:
            self._expect(Token.KW_LOOP)
        else:
            self._accept(Token.KW_LOOP)

        loop_body = self._parse_block()

        then_clause = None
        until_clause = None

        if self._peek() == Token.NODENT:
            if self._peek_ahead() == Token.KW_THEN:
                self._accept(Token.NODENT)
                self._accept(Token.KW_THEN)
                then_clause = self._parse_expr()

            if self._peek_ahead() == Token.KW_UNTIL:
                self._accept(Token.NODENT)
                self._accept(Token.KW_UNTIL)
                until_clause = self._parse_condition()

        return LoopStatementNode(
            for_clause,
            each_clause,
            while_clause,
            loop_body,
            then_clause,
            until_clause
        )

    def _parse_condition(self):
        return self._parse_condition_prec6()

    def _parse_condition_prec6(self):
        lhs = self._parse_condition_prec5()

        while self._accept(Token.OP_OR):
            lhs = OrNode(lhs, self._parse_condition_prec5())

        return lhs

    def _parse_condition_prec5(self):
        lhs = self._parse_condition_prec4()

        while self._accept(Token.OP_XOR):
            lhs = XorNode(lhs, self._parse_condition_prec4())

        return lhs

    def _parse_condition_prec4(self):
        lhs = self._parse_condition_prec3()

        while self._accept(Token.OP_AND):
            lhs = AndNode(lhs, self._parse_condition_prec3())

        return lhs

    def _parse_condition_prec3(self):
        def _accept():
            if self._accept(Token.OP_EQ) or self._accept(Token.OP_NEQ):
                return True
            else:
                return False

        lhs = self._parse_condition_prec2()

        while _accept():
            id = self._current.id

            if id == Token.OP_EQ:
                lhs = EqlNode(lhs, self._parse_condition_prec2())
            elif id == Token.OP_NEQ:
                lhs = NeqNode(lhs, self._parse_condition_prec2())
            else:
                raise CompilerBug("~.~")

        return lhs

    def _parse_condition_prec2(self):
        def _accept():
            if self._accept('<') or self._accept('>'):
                return True
            elif self._accept(Token.OP_LEQ) or self._accept(Token.OP_GEQ):
                return True
            else:
                return False

        lhs = self._parse_condition_prec1()

        while _accept():
            id = self._current.id

            if id == '<':
                lhs = LtnNode(lhs, self._parse_condition_prec1())
            elif id == '>':
                lhs = GtnNode(lhs, self._parse_condition_prec1())
            elif id == Token.OP_LEQ:
                lhs = LeqNode(lhs, self._parse_condition_prec1())
            elif id == Token.OP_GEQ:
                lhs = GeqNode(lhs, self._parse_condition_prec1())
            else:
                raise CompilerBug("8.8")

        return lhs

    def _parse_condition_prec1(self):
        def _accept():
            if self._accept(Token.OP_NOT):
                return True

        if _accept():
            id = self._current.id

            if id == Token.OP_NOT:
                return NotNode(self._parse_condition_prec1())
            else:
                raise CompilerBug("%.%")
        else:
            return self._parse_expr()

    def _parse_expr(self):
        return self._parse_expr_prec13()

    def _parse_expr_prec13(self):
        lhs = self._parse_expr_prec12()

        if self._accept(':'):
            return InitExprNode(lhs, self._parse_expr_prec13())
        elif self._accept('='):
            return AssignExprNode(lhs, self._parse_expr_prec13())

        elif self._accept(Token.OP_ADD_ASSIGN):
            return AddAssignExprNode(lhs, self._parse_expr_prec13())

        elif self._accept(Token.OP_SUB_ASSIGN):
            return SubAssignExprNode(lhs, self._parse_expr_prec13())
        elif self._accept(Token.OP_MUL_ASSIGN):
            return MulAssignExprNode(lhs, self._parse_expr_prec13())
        elif self._accept(Token.OP_DIV_ASSIGN):
            return DivAssignExprNode(lhs, self._parse_expr_prec13())
        elif self._accept(Token.OP_MOD_ASSIGN):
            return ModAssignExprNode(lhs, self._parse_expr_prec13())

        elif self._accept(Token.OP_AND_ASSIGN):
            return BitAndAssignExprNode(lhs, self._parse_expr_prec13())
        elif self._accept(Token.OP_XOR_ASSIGN):
            return BitXorAssignExprNode(lhs, self._parse_expr_prec13())
        elif self._accept(Token.OP_OR_ASSIGN):
            return BitOrAssignExprNode(lhs, self._parse_expr_prec13())
        elif self._accept(Token.OP_SHL_ASSIGN):
            return BitShlAssignExprNode(lhs, self._parse_expr_prec13())
        elif self._accept(Token.OP_SHR_ASSIGN):
            return BitShrAssignExprNode(lhs, self._parse_expr_prec13())

        else:
            return lhs

    def _parse_expr_prec12(self):
        lhs = self._parse_expr_prec11()

        if self._accept(Token.KW_IF):
            condition = self._parse_condition()

            self._expect(Token.KW_ELSE)

            rhs = self._parse_expr_prec11()

            return TernaryConditionalNode(lhs, condition, rhs)

        else:
            return lhs

    def _parse_expr_prec11(self):
        lhs = self._parse_expr_prec10()

        while self._accept('|'):
            lhs = BitOrExprNode(lhs, self._parse_expr_prec10())

        return lhs

    def _parse_expr_prec10(self):
        lhs = self._parse_expr_prec9()

        while self._accept('^'):
            lhs = BitXorExprNode(lhs, self._parse_expr_prec9())

        return lhs

    def _parse_expr_prec9(self):
        lhs = self._parse_expr_prec8()

        while self._accept('&'):
            lhs = BitAndExprNode(lhs, self._parse_expr_prec8())

        return lhs

    def _parse_expr_prec8(self):
        def _accept():
            if self._accept(Token.OP_SHL) or self._accept(Token.OP_SHR):
                return True
            else:
                return False

        lhs = self._parse_expr_prec7()

        while _accept():
            id = self._current.id

            if id == Token.OP_SHL:
                lhs = BitShlExprNode(lhs, self._parse_expr_prec7())
            elif id == Token.OP_SHR:
                lhs = BitShrExprNode(lhs, self._parse_expr_prec7())
            else:
                raise CompilerBug("^.^")

        return lhs

    def _parse_expr_prec7(self):
        def _accept():
            if self._accept('+') or self._accept('-'):
                return True
            else:
                return False

        lhs = self._parse_expr_prec6()

        while _accept():
            id = self._current.id

            if id == '+':
                lhs = AddExprNode(lhs, self._parse_expr_prec6())
            elif id == '-':
                lhs = SubExprNode(lhs, self._parse_expr_prec6())
            else:
                raise CompilerBug("*_*")

        return lhs

    def _parse_expr_prec6(self):
        def _accept():
            if self._accept('*') or self._accept('/') or self._accept('%'):
                return True
            else:
                return False

        lhs = self._parse_expr_prec5()

        while _accept():
            id = self._current.id

            if id == '*':
                lhs = MulExprNode(lhs, self._parse_expr_prec5())
            elif id == '/':
                lhs = DivExprNode(lhs, self._parse_expr_prec5())
            elif id == '%':
                lhs = ModExprNode(lhs, self._parse_expr_prec5())
            else:
                raise CompilerBug("$_$")

        return lhs

    def _parse_expr_prec5(self):
        def _accept():
            if self._accept(Token.OP_AS):
                return True
            else:
                return False

        lhs = self._parse_expr_prec4()

        while _accept():
            id = self._current.id

            if id == Token.OP_AS:
                lhs = AsNode(lhs, self._parse_expr_prec4())
            else:
                raise CompilerBug("$_#")

        return lhs

    def _parse_expr_prec4(self):
        def _accept():
            if self._accept('.'): return True
            else:
                return False

        lhs = self._parse_expr_prec3()

        while _accept():
            id = self._current.id

            if id == '.':
                lhs = DotExprNode(lhs, self._parse_expr_prec3())
            else:
                raise CompilerBug("%.%")

        return lhs

    def _parse_expr_prec3(self):
        def _accept():
            if self._accept('('):
                return True
            elif self._accept('['):
                return True
            elif self._accept(Token.OP_INC):
                return True
            elif self._accept(Token.OP_DEC):
                return True
            else:
                return False

        lhs = self._parse_expr_prec2()

        while _accept():
            id = self._current.id

            if id == '(':
                args = [ ]

                if not self._accept(')'):
                    while True:
                        args.append(self._parse_expr())
                        if not self._accept(','):
                            self._expect(')')
                            break

                lhs = CallExprNode(lhs, args)

            elif id == '[':
                expr = self._parse_expr()

                self._expect(']')

                lhs = IndexExprNode(lhs, expr)

            elif id == Token.OP_INC:
                lhs = PostIncExprNode(lhs)

            elif id == Token.OP_DEC:
                lhs = PostDecExprNode(lhs)

            else:
                raise CompilerBug("O_o")

        return lhs

    def _parse_expr_prec2(self):
        if self._accept('*'):
            return PtrExprNode(self._parse_expr_prec2())

        elif self._accept('&'):
            return RefExprNode(self._parse_expr_prec2())

        elif self._accept('-'):
            return NegExprNode(self._parse_expr_prec2())

        elif self._accept(Token.OP_INC):
            return PreIncExprNode(self._parse_expr_prec2())

        elif self._accept(Token.OP_DEC):
            return PreDecExprNode(self._parse_expr_prec2())

        elif self._accept('~'):
            return BitNotExprNode(self._parse_expr_prec2())

        elif self._accept('['):
            length = self._parse_expr()
            self._expect(']')
            return ArrayTypeNode(length, self._parse_expr_prec2())

        else:
            return self._parse_expr_prec1()

    def _parse_expr_prec1(self):
        _accept = self._accept

        if _accept(Token.ID):
            return SymbolNode(self._current.value)

        elif _accept('('):
            expr = self._parse_expr()
            self._expect(')')
            return expr

        elif _accept(Token.LT_INT_DEC):
            return AutoIntNode(self._current.value, radix=10)

        elif _accept(Token.LT_INT_BIN):
            return AutoIntNode(self._current.value, radix=2)

        elif _accept(Token.LT_TRUE):
            return IntNode(1, False, 1)

        elif _accept(Token.LT_FALSE):
            return IntNode(1, False, 0)

        elif _accept(Token.LT_NIL):
            return NilNode()

        elif _accept(Token.LT_STRING):
            return StringNode(self._current.value)

        elif _accept(Token.LT_CHAR):
            return IntNode(8, False, ord(self._current.value))

        elif _accept(Token.KW_BIT):
            return IntTypeNode(1, False)

        elif _accept(Token.KW_CHAR):
            return IntTypeNode(8, False)

        elif _accept(Token.KW_BYTE):
            return IntTypeNode(8, True)

        elif _accept(Token.KW_SHORT):
            return IntTypeNode(16, True)

        elif _accept(Token.KW_INT):
            return IntTypeNode(32, True)

        elif _accept(Token.KW_LONG):
            return IntTypeNode(64, True)

        elif _accept(Token.KW_UBYTE):
            return IntTypeNode(8, False)

        elif _accept(Token.KW_USHORT):
            return IntTypeNode(16, False)

        elif _accept(Token.KW_UINT):
            return IntTypeNode(32, False)

        elif _accept(Token.KW_ULONG):
            return IntTypeNode(64, False)

        else:
            if self._peek() == Token.KW_STRUCT:
                return self._parse_struct()

            elif self._peek() == Token.KW_EXTERN:
                return self._parse_fun()

            else:
                raise UnexpectedToken(self._next)
