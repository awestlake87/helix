
from .token import Token
from ..err import UnexpectedChar, Todo

class Lexer:
    NORMAL              = 0
    DEDENTING           = 1
    FRESH_LINE          = 2

    def __init__(self, str):
        self._input = str
        self._input_len = len(self._input)
        self._cursor = 0

        self._column = 1
        self._line = 1

        self._state = Lexer.FRESH_LINE

        self._indents = [ 0 ]

    def _peek(self):
        if self._cursor >= self._input_len:
            return '\0'
        else:
            return self._input[self._cursor]

    def _toss(self):
        c = self._peek()

        if c == '\n':
            self._line += 1
            self._column = 1
            self._state = Lexer.FRESH_LINE
        elif c == '\t':
            assert False
        else:
            self._column += 1

        self._cursor += 1

        return c

    def _take(self):
        self._token += self._toss()

    def _accept(self, c):
        if self._peek() == c:
            self._take()
            return True
        else:
            return False

    def scan(self):
        self._token = ""

        while self._peek() == ' ' or self._peek() == '\n':
            self._toss()


        if self._peek() == '\0' and self._state != Lexer.DEDENTING:
            self._state = Lexer.DEDENTING
            self._column = 0

        if self._state == Lexer.FRESH_LINE:

            if self._column == self._indents[-1]:
                self._state = Lexer.NORMAL
                return Token(Token.NODENT)

            elif self._column > self._indents[-1]:
                self._indents.append(self._column)
                self._state = Lexer.NORMAL
                return Token(Token.INDENT)

            else:
                self._state = Lexer.DEDENTING
                self._indents.pop()
                return Token(Token.DEDENT)

        elif self._state == Lexer.DEDENTING:

            if self._column < self._indents[-1]:
                self._indents.pop()
                return Token(Token.DEDENT)

            elif self._column == self._indents[-1]:
                self._state = Lexer.NORMAL

                if self._peek() == '\0':
                    return Token(Token.END)

            else:
                raise Exception("invalid indents")

        c = self._peek()

        if c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z':
            return self._scan_alpha()
        elif c >= '0' and c <= '9':
            return self._scan_num()
        else:
            return self._scan_punct()


    def _scan_num(self):
        def _take_dec_digits():
            c = self._peek()
            while c >= '0' and c <= '9':
                self._take()
                c = self._peek()

        def _end_int_dec():
            c = self._peek()
            if (
                c >= 'a' and c <= 'z' or
                c >= 'A' and c <= 'Z' or
                c >= '0' and c <= '9' or
                c == '_'
            ):
                raise UnexpectedChar(c)

            else:
                return Token(Token.LT_INT_DEC, self._token)

        c = self._peek()

        if c == '0':
            self._take()
            return _end_int_dec()
        elif c >= '0' and c <= '9':
            _take_dec_digits()
            return _end_int_dec()
        else:
            raise UnexpectedChar(c)


    def _scan_punct(self):
        c = self._peek()

        if c == '(':
            return Token(self._toss())
        elif c == ')':
            return Token(self._toss())
        elif c == '*':
            return Token(self._toss())
        elif c == ',':
            return Token(self._toss())
        elif c == '=':
            return Token(self._toss())

        elif c == ':':
            self._toss()
            if self._peek() == '=':
                self._toss()
                return Token(Token.OP_UPSERT)
            else:
                return Token(':')

        elif c == '.':
            self._toss()
            if self._peek() == '.':
                self._toss()
                if self._peek() == '.':
                    self._toss()
                    return Token(Token.OP_SPREAD)
                else:
                    return Token(Token.OP_RANGE)
            else:
                return Token('.')

        else:
            raise UnexpectedChar(c)

    def _scan_alpha(self):
        def _end_id():
            c = self._peek()
            while (
                c >= 'a' and c <= 'z' or
                c >= 'A' and c <= 'Z' or
                c >= '0' and c <= '9' or
                c == '_'
            ):
                self._take()
                c = self._peek()

            return Token(Token.ID, self._token)

        def _end_kw(id):
            c = self._peek()
            if (
                c >= 'a' and c <= 'z' or
                c >= 'A' and c <= 'Z' or
                c >= '0' and c <= '9' or
                c == '_'
            ):
                return _end_id()
            else:
                return Token(id)


        _accept = self._accept

        if _accept('b'):
            if _accept('i'):
                if _accept('t'):
                    return _end_kw(Token.KW_BIT)

            elif _accept('y'):
                if _accept('t'):
                    if _accept('e'):
                        return _end_kw(Token.KW_BYTE)
        elif _accept('c'):
            if _accept('a'):
                if _accept('s'):
                    if _accept('e'):
                        return _end_kw(Token.KW_CASE)

            elif _accept('h'):
                if _accept('a'):
                    if _accept('r'):
                        return _end_kw(Token.KW_CHAR)

        elif _accept('d'):
            if _accept('e'):
                if _accept('f'):
                    if _accept('a'):
                        if _accept('u'):
                            if _accept('l'):
                                if _accept('t'):
                                    return _end_kw(Token.KW_DEFAULT)
            elif _accept('o'):
                return _end_kw(Token.KW_DO)

        elif _accept('e'):
            if _accept('l'):
                if _accept('i'):
                    if _accept('f'):
                        return _end_kw(Token.KW_ELIF)

                elif _accept('s'):
                    if _accept('e'):
                        return _end_kw(Token.KW_ELSE)

            elif _accept('x'):
                if _accept('t'):
                    if _accept('e'):
                        if _accept('r'):
                            if _accept('n'):
                                return _end_kw(Token.KW_EXTERN)
        elif _accept('f'):
            if _accept('a'):
                if _accept('l'):
                    if _accept('s'):
                        if _accept('e'):
                            return _end_kw(Token.KW_FALSE)

            elif _accept('u'):
                if _accept('n'):
                    return _end_kw(Token.KW_FUN)

        elif _accept('g'):
            if _accept('l'):
                if _accept('o'):
                    if _accept('b'):
                        if _accept('a'):
                            if _accept('l'):
                                return _end_kw(Token.KW_GLOBAL)


        elif _accept('i'):
            if _accept('f'):
                return _end_kw(Token.KW_IF)

            elif _accept('n'):
                if _accept('t'):
                    if _accept('e'):
                        if _accept('r'):
                            if _accept('n'):
                                return _end_kw(Token.KW_INTERN)

                    else:
                        return _end_kw(Token.KW_INT)

        elif _accept('l'):
            if _accept('o'):
                if _accept('n'):
                    if _accept('g'):
                        return _end_kw(Token.KW_LONG)

        elif _accept('n'):
            if _accept('i'):
                if _accept('l'):
                    return _end_kw(Token.LT_NIL)

        elif _accept('p'):
            if _accept('a'):
                if _accept('s'):
                    if _accept('s'):
                        return _end_kw(Token.KW_PASS)

        elif _accept('r'):
            if _accept('e'):
                if _accept('t'):
                    if _accept('u'):
                        if _accept('r'):
                            if _accept('n'):
                                return _end_kw(Token.KW_RETURN)

        elif _accept('s'):
            if _accept('h'):
                if _accept('o'):
                    if _accept('r'):
                        if _accept('t'):
                            return _end_kw(Token.KW_SHORT)

            elif _accept('t'):
                if _accept('r'):
                    if _accept('u'):
                        if _accept('c'):
                            if _accept('t'):
                                return _end_kw(Token.KW_STRUCT)

            elif _accept('w'):
                if _accept('i'):
                    if _accept('t'):
                        if _accept('c'):
                            if _accept('h'):
                                return _end_kw(Token.KW_SWITCH)

        elif _accept('t'):
            if _accept('h'):
                if _accept('e'):
                    if _accept('n'):
                        return _end_kw(Token.KW_THEN)

            elif _accept('r'):
                if _accept('u'):
                    if _accept('e'):
                        return _end_kw(Token.LT_TRUE)

        elif _accept('u'):
            if _accept('b'):
                if _accept('y'):
                    if _accept('t'):
                        if _accept('e'):
                            return _end_kw(Token.KW_UBYTE)

            elif _accept('i'):
                if _accept('n'):
                    if _accept('t'):
                        return _end_kw(Token.KW_UINT)

            elif _accept('l'):
                if _accept('o'):
                    if _accept('n'):
                        if _accept('g'):
                            return _end_kw(Token.KW_ULONG)

            elif _accept('s'):
                if _accept('h'):
                    if _accept('o'):
                        if _accept('r'):
                            if _accept('t'):
                                return _end_kw(Token.KW_USHORT)



        return _end_id()
