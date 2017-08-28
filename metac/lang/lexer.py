
from .token import Token
from ..err import UnexpectedChar, Todo

def scan_tokens(code):
    lexer = Lexer(code)
    token = lexer.scan()

    while token != Token.END:
        yield token
        token = lexer.scan()

    # keep yielding END tokens
    while True:
        yield token

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
            raise Todo()

        else:
            self._column += 1

        self._cursor += 1

        return c

    def _take(self):
        c = self._toss()

        self._token += c

        return c

    def _accept(self, c):
        if self._peek() == c:
            self._take()
            return True
        else:
            return False

    def _ignore_space_and_comments(self):
        while True:
            while self._peek() == ' ' or self._peek() == '\n':
                self._toss()

            if self._peek() == '#':
                while self._peek() != '\n' and self._peek() != '\0':
                    self._toss()
            else:
                return

    def scan(self):
        self._token = ""

        self._ignore_space_and_comments()

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
                    return Token(Token.NODENT)

            else:
                raise Exception("invalid indents")


        c = self._peek()

        if c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c == '_':
            return self._scan_alpha()

        elif c >= '0' and c <= '9':
            return self._scan_num()

        elif c == '@':
            return self._scan_attribute()

        elif c == '"':
            return self._scan_string()

        elif c == '\'':
            return self._scan_char()

        else:
            return self._scan_punct()

    def _scan_string(self):
        quote = self._toss()
        assert quote == '"'

        value = ""

        while True:
            c = self._toss()

            if c == '"':
                break

            elif c == '\\':
                c = self._toss()

                if c == '\\':
                    value += '\\'
                elif c == '"':
                    value += '"'
                elif c == 'a':
                    value += '\a'
                elif c == 'b':
                    value += '\b'
                elif c == 'f':
                    value += '\f'
                elif c == 'n':
                    value += '\n'
                elif c == 'r':
                    value += '\r'
                elif c == 't':
                    value += '\t'
                elif c == 'v':
                    value += '\v'
                else:
                    raise Todo()

            elif c == '\n':
                raise Todo("expected \"")
            else:
                value += c

        return Token(Token.LT_STRING, value)

    def _scan_char(self):
        quote = self._toss()
        assert quote == '\''

        c = self._toss()
        value = None

        if c == '\'':
            raise Todo("empty '' is not a valid char")

        elif c == '\\':
            c = self._toss()

            if c == '\\':
                value = '\\'
            elif c == '\'':
                value = '\''
            elif c == 'a':
                value = '\a'
            elif c == 'b':
                value = '\b'
            elif c == 'f':
                value = '\f'
            elif c == 'n':
                value = '\n'
            elif c == 'r':
                value = '\r'
            elif c == 't':
                value = '\t'
            elif c == 'v':
                value = '\v'
            else:
                raise Todo()

        elif c == '\n':
            raise Todo("unexpected end of line {}".format(self._line - 1))
        else:
            value = c


        if self._toss() != '\'':
            raise Todo(
                "expected ' after char at line {}".format(self._line)
            )

        return Token(Token.LT_CHAR, value)

    def _scan_attribute(self):
        prefix = self._toss()
        assert prefix == '@'

        c = self._peek()

        if c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c == '_':
            self._take()

        else:
            raise UnexpectedChar(c)

        c = self._peek()

        while (
            c >= 'a' and c <= 'z' or
            c >= 'A' and c <= 'Z' or
            c >= '0' and c <= '9' or
            c == '_'
        ):
            self._take()
            c = self._peek()

        return Token(Token.ATTR_ID, self._token)

    def _scan_num(self):
        def _accept_dec_digits():
            c = self._peek()
            while c >= '0' and c <= '9':
                self._take()
                c = self._peek()

        def _accept_bin_digits():
            while self._accept('0') or self._accept('1'):
                pass

        def _end_int(id):
            c = self._peek()
            if (
                c >= 'a' and c <= 'z' or
                c >= 'A' and c <= 'Z' or
                c >= '0' and c <= '9' or
                c == '_'
            ):
                raise UnexpectedChar(c)

            else:
                if len(self._token) > 0:
                    return Token(id, self._token)
                else:
                    raise Todo("make an error for this")

        c = self._peek()

        if self._accept('0'):
            if self._accept('b'):
                self._token = ""
                _accept_bin_digits()

                return _end_int(Token.LT_INT_BIN)
            else:
                return _end_int(Token.LT_INT_DEC)

        elif c >= '0' and c <= '9':
            _accept_dec_digits()
            return _end_int(Token.LT_INT_DEC)

        else:
            raise UnexpectedChar(c)


    def _scan_punct(self):
        def _toss(c):
            if self._peek() == c:
                self._toss()
                return True
            else:
                return False

        if _toss('('):
            return Token('(')
        elif _toss(')'):
            return Token(')')

        elif _toss('['):
            return Token('[')
        elif _toss(']'):
            return Token(']')

        elif _toss(','):
            return Token(',')

        elif _toss('='):
            if _toss('='):
                return Token(Token.OP_EQ)
            else:
                return Token('=')

        elif _toss('!'):
            if _toss('='):
                return Token(Token.OP_NEQ)

        elif _toss(':'):
            return Token(':')

        elif _toss('.'):
            if _toss('.'):
                if _toss('.'):
                    return Token(Token.OP_SPREAD)
                else:
                    return Token(Token.OP_RANGE)
            else:
                return Token('.')

        elif _toss('+'):
            if _toss('+'):
                return Token(Token.OP_INC)
            elif _toss('='):
                return Token(Token.OP_ADD_ASSIGN)
            else:
                return Token('+')

        elif _toss('-'):
            if _toss('-'):
                return Token(Token.OP_DEC)
            elif _toss('='):
                return Token(Token.OP_SUB_ASSIGN)
            else:
                return Token('-')

        elif _toss('*'):
            if _toss('='):
                return Token(Token.OP_MUL_ASSIGN)
            else:
                return Token('*')

        elif _toss('/'):
            if _toss('='):
                return Token(Token.OP_DIV_ASSIGN)
            else:
                return Token('/')

        elif _toss('%'):
            if _toss('='):
                return Token(Token.OP_MOD_ASSIGN)
            else:
                return Token('%')

        elif _toss('&'):
            if _toss('='):
                return Token(Token.OP_AND_ASSIGN)
            else:
                return Token('&')

        elif _toss('^'):
            if _toss('='):
                return Token(Token.OP_XOR_ASSIGN)
            else:
                return Token('^')

        elif _toss('|'):
            if _toss('='):
                return Token(Token.OP_OR_ASSIGN)
            else:
                return Token('|')


        elif _toss('~'):
            return Token('~')

        elif _toss('<'):
            if _toss('='):
                return Token(Token.OP_LEQ)
            elif _toss('<'):
                if _toss('='):
                    return Token(Token.OP_SHL_ASSIGN)
                else:
                    return Token(Token.OP_SHL)
            else:
                return Token('<')

        elif _toss('>'):
            if _toss('='):
                return Token(Token.OP_GEQ)
            elif _toss('>'):
                if _toss('='):
                    return Token(Token.OP_SHR_ASSIGN)
                else:
                    return Token(Token.OP_SHR)
            else:
                return Token('>')

        else:
            raise UnexpectedChar(self._peek())

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

        if _accept('a'):
            if _accept('n'):
                if _accept('d'):
                    return _end_kw(Token.OP_AND)

            elif _accept('s'):
                return _end_kw(Token.OP_AS)

            elif _accept('u'):
                if _accept('t'):
                    if _accept('o'):
                        return _end_kw(Token.KW_AUTO)

        elif _accept('b'):
            if _accept('i'):
                if _accept('t'):
                    if _accept('c'):
                        if _accept('a'):
                            if _accept('s'):
                                if _accept('t'):
                                    return _end_kw(Token.OP_BITCAST)
                    else:
                        return _end_kw(Token.KW_BIT)

            elif _accept('r'):
                if _accept('e'):
                    if _accept('a'):
                        if _accept('k'):
                            return _end_kw(Token.KW_BREAK)

            elif _accept('y'):
                if _accept('t'):
                    if _accept('e'):
                        return _end_kw(Token.KW_BYTE)
        elif _accept('c'):
            if _accept('a'):
                if _accept('s'):
                    if _accept('e'):
                        return _end_kw(Token.KW_CASE)

                    elif _accept('t'):
                        return _end_kw(Token.OP_CAST)

                elif _accept('t'):
                    if _accept('c'):
                        if _accept('h'):
                            return _end_kw(Token.KW_CATCH)

            elif _accept('f'):
                if _accept('u'):
                    if _accept('n'):
                        return _end_kw(Token.KW_CFUN)

            elif _accept('g'):
                if _accept('l'):
                    if _accept('o'):
                        if _accept('b'):
                            if _accept('a'):
                                if _accept('l'):
                                    return _end_kw(Token.KW_CGLOBAL)

            elif _accept('h'):
                if _accept('a'):
                    if _accept('r'):
                        return _end_kw(Token.KW_CHAR)

            elif _accept('o'):
                if _accept('n'):
                    if _accept('t'):
                        if _accept('i'):
                            if _accept('n'):
                                if _accept('u'):
                                    if _accept('e'):
                                        return _end_kw(Token.KW_CONTINUE)

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
            if _accept('a'):
                if _accept('c'):
                    if _accept('h'):
                        return _end_kw(Token.KW_EACH)

            elif _accept('l'):
                if _accept('i'):
                    if _accept('f'):
                        return _end_kw(Token.KW_ELIF)

                elif _accept('s'):
                    if _accept('e'):
                        return _end_kw(Token.KW_ELSE)

            elif _accept('x'):
                if _accept('p'):
                    if _accept('o'):
                        if _accept('r'):
                            if _accept('t'):
                                return _end_kw(Token.KW_EXPORT)
        elif _accept('f'):
            if _accept('a'):
                if _accept('l'):
                    if _accept('s'):
                        if _accept('e'):
                            return _end_kw(Token.LT_FALSE)

            elif _accept('o'):
                if _accept('r'):
                    return _end_kw(Token.KW_FOR)

            elif _accept('r'):
                if _accept('o'):
                    if _accept('m'):
                        return _end_kw(Token.KW_FROM)

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

            elif _accept('m'):
                if _accept('p'):
                    if _accept('o'):
                        if _accept('r'):
                            if _accept('t'):
                                return _end_kw(Token.KW_IMPORT)

            elif _accept('n'):
                if _accept('t'):
                    return _end_kw(Token.KW_INT)

        elif _accept('l'):
            if _accept('i'):
                if _accept('n'):
                    if _accept('k'):
                        return _end_kw(Token.KW_LINK)

            elif _accept('o'):
                if _accept('n'):
                    if _accept('g'):
                        return _end_kw(Token.KW_LONG)

                elif _accept('o'):
                    if _accept('p'):
                        return _end_kw(Token.KW_LOOP)

        elif _accept('n'):
            if _accept('i'):
                if _accept('l'):
                    return _end_kw(Token.LT_NIL)

            elif _accept('o'):
                if _accept('t'):
                    return _end_kw(Token.OP_NOT)

        elif _accept('o'):
            if _accept('f'):
                if _accept('f'):
                    if _accept('s'):
                        if _accept('e'):
                            if _accept('t'):
                                if _accept('o'):
                                    if _accept('f'):
                                        return _end_kw(Token.OP_OFFSETOF)

            elif _accept('r'):
                return _end_kw(Token.OP_OR)

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

            elif _accept('i'):
                if _accept('z'):
                    if _accept('e'):
                        if _accept('o'):
                            if _accept('f'):
                                return _end_kw(Token.OP_SIZEOF)

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
                    if _accept('o'):
                        if _accept('w'):
                            return _end_kw(Token.KW_THROW)

            elif _accept('r'):
                if _accept('u'):
                    if _accept('e'):
                        return _end_kw(Token.LT_TRUE)

                elif _accept('y'):
                    return _end_kw(Token.KW_TRY)

            elif _accept('y'):
                if _accept('p'):
                    if _accept('e'):
                        if _accept('o'):
                            if _accept('f'):
                                return _end_kw(Token.OP_TYPEOF)

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

            elif _accept('n'):
                if _accept('t'):
                    if _accept('i'):
                        if _accept('l'):
                            return _end_kw(Token.KW_UNTIL)

            elif _accept('s'):
                if _accept('h'):
                    if _accept('o'):
                        if _accept('r'):
                            if _accept('t'):
                                return _end_kw(Token.KW_USHORT)

        elif _accept('v'):
            if _accept('a'):
                if _accept('r'):
                    if _accept('g'):
                        if _accept('s'):
                            return _end_kw(Token.KW_VARGS)
            elif _accept('o'):
                if _accept('i'):
                    if _accept('d'):
                        return _end_kw(Token.KW_VOID)

        elif _accept('w'):
            if _accept('h'):
                if _accept('i'):
                    if _accept('l'):
                        if _accept('e'):
                            return _end_kw(Token.KW_WHILE)

        elif _accept('x'):
            if _accept('o'):
                if _accept('r'):
                    return _end_kw(Token.OP_XOR)

        return _end_id()
