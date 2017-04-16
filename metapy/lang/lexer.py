
from .token import Token

class Lexer:
    _ID_CHRS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"


    def __init__(self, str):
        self._input = str
        self._input_len = len(self._input)
        self._cursor = 0

    def _peek(self):
        if self._cursor >= self._input_len:
            return '\0'
        else:
            return self._input[self._cursor]

    def _toss(self):
        c = self._peek()

        if self._cursor < self._input_len:
            self._cursor += 1

        return c

    def _take(self):
        self._token += self._toss()

    def scan(self):
        self._token = ""

        while self._token == ' ':
            self._toss()


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
        def _end_identifier():
            c = self._peek()
            while c in Lexer._ID_CHRS:
                self._take()

            return Token(Token.ID, self._token)

        return _end_identifier()

    def _scan_num(self):
        assert False

    def _scan_punct(self):
        assert False
