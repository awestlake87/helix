from .lexer import Lexer

class Parser:
    def __init__(self, str):
        self._lexer = Lexer(str)
