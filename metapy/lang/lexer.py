
from .token import Token

class Lexer:
    NORMAL              = 0
    STATE_DEDENTING     = 1
    STATE_FRESH_LINE    = 2

    def __init__(self, str):
        self._input = str
        self._input_len = len(self._input)
        self._cursor = 0

        self._column = 1
        self._line = 1

        self._state = Lexer.STATE_FRESH_LINE

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


        if self._peek() == '\0' and self._state != Lexer.STATE_DEDENTING:
            self._state = Lexer.STATE_DEDENTING
            self._column = 0
            return Token(Token.END)



        c = self._peek()

        if c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z':
            return self._scan_alpha()
        elif c >= '0' and c <= '9':
            return self._scan_num()
        elif c == '.':
            return self._scan_num()
        else:
            return self._scan_punct()


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


        if _accept('e'):
            if _accept('x'):
                if _accept('t'):
                    if _accept('e'):
                        if _accept('r'):
                            if _accept('n'):
                                return _end_kw(Token.KW_EXTERN)
        elif _accept('f'):
            if _accept('u'):
                if _accept('n'):
                    return _end_kw(Token.KW_FUN)

        elif _accept('i'):
            if _accept('n'):
                if _accept('t'):
                    if _accept('e'):
                        if _accept('r'):
                            if _accept('n'):
                                return _end_kw(Token.KW_INTERN)
        


        return _end_id()

    def _scan_num(self):
        assert False

    def _scan_punct(self):
        _accept = self._accept

        if _accept('('):
            return Token('(')
        elif _accept(')'):
            return Token(')')
