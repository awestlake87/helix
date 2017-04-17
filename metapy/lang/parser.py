from .lexer import Lexer
from .token import Token

class Parser:
    def __init__(self, str):
        self._lexer = Lexer(str)

    def parse(self):

        token = self._lexer.scan()

        while token.id != Token.END:
            print(token)
            token = self._lexer.scan()
