
from metapy.lang.lexer import Lexer

if __name__ == "__main__":
    lexer = Lexer(input("Enter a string to lex: "))

    while True:
        token = lexer.scan()

        print(token)
