from .lexer import Lexer
from .token import Token

from ..ast import *
from ..err import Todo, ExpectedToken, UnexpectedToken, CompilerBug

class Parser:
    def __init__(self, str):
        self._lexer = Lexer(str)
        self._current = Token(Token.NONE)
        self._next = self._lexer.scan()

    def parse(self):
        unit = self._parse_unit()

        self._expect(Token.END)

        return unit

    def _peek(self):
        return self._next.id

    def _expect(self, id):
        if not self._accept(id):
            raise ExpectedToken(Token(id), self._next)

    def _accept(self, id):
        if self._next.id == id:
            self._current = self._next
            self._next = self._lexer.scan()
            return True
        else:
            return False

    def _parse_unit(self):
        return UnitNode(self._parse_block())

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
                case_value = self._parse_expr()
                case_block = self._parse_block()
                case_branches.append((case_value, case_block))

            if self._accept(Token.KW_DEFAULT):
                default_block = self._parse_block()

            self._expect(Token.DEDENT)
            return SwitchStatementNode(value, case_branches, default_block)

    def _parse_if_statement(self):
        self._expect(Token.KW_IF)

        if_cond = self._parse_condition()
        if_block = self._parse_block()

        if_branches = [ ]

        if_branches.append((if_cond, if_block))

        while self._accept(Token.KW_ELIF):
            cond = self._parse_condition()
            block = self._parse_block()
            if_branches.append((cond, block))

        if self._accept(Token.KW_ELSE):
            return IfStatementNode(if_branches, self._parse_block())
        else:
            return IfStatementNode(if_branches)


    def _parse_fun(self, linkage):
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
                linkage,
                self._parse_block()
            )
        else:
            return FunNode(
                FunTypeNode(ret_type, param_types),
                id,
                param_ids,
                linkage
            )

    def _parse_condition(self):
        return self._parse_expr()

    def _parse_expr(self):
        return self._parse_expr_prec4()

    def _parse_expr_prec4(self):
        def _accept():
            if self._accept(':'):
                return True
            elif self._accept('='):
                return True
            else:
                return False

        lhs = self._parse_expr_prec3()

        if _accept():
            id = self._current.id

            if id == ':':
                return InitExprNode(lhs, self._parse_expr_prec4())
            elif id == '=':
                return AssignExprNode(lhs, self._parse_expr_prec4())
            else:
                raise CompilerBug("0_0")

        else:
            return lhs

    def _parse_expr_prec3(self):
        def _accept():
            if self._accept('('):
                return True
            else:
                return False

        lhs = self._parse_expr_prec2()

        while _accept():
            id = self._current.id

            if id == '(':
                args = [ ]

                while True:
                    args.append(self._parse_expr())
                    if not self._accept(','):
                        self._expect(')')
                        break

                lhs = CallExprNode(lhs, args)
            else:
                raise CompilerBug("O_o")

        return lhs

    def _parse_expr_prec2(self):
        def _accept():
            if self._accept('*'):
                return True
            else:
                return False

        if _accept():
            id = self._current.id

            if id == '*':
                return PtrExprNode(self._parse_expr_prec2())
            else:
                raise CompilerBug("O_O")

        return self._parse_expr_prec1()

    def _parse_expr_prec1(self):
        _accept = self._accept

        if _accept(Token.ID):
            return SymbolNode(self._current.value)

        elif _accept('('):
            expr = self._parse_expr()
            self._expect(')')
            return expr

        elif _accept(Token.KW_EXTERN):
            return self._parse_fun(FunNode.EXTERN_C)

        elif _accept(Token.KW_INTERN):
            return self._parse_fun(FunNode.INTERN_C)

        elif _accept(Token.LT_INT_DEC):
            return AutoIntNode(self._current.value)

        elif _accept(Token.LT_TRUE):
            return IntNode(1, False, 1)

        elif _accept(Token.LT_FALSE):
            return IntNode(1, False, 0)

        elif _accept(Token.LT_NIL):
            return NilNode()

        elif _accept(Token.KW_BIT):
            return IntTypeNode(1, False)

        elif _accept(Token.KW_CHAR):
            return IntTypeNode(8, True)

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
            raise UnexpectedToken(self._next)
