
#!/usr/bin/python3

from metapy.lang import Parser

if __name__ == "__main__":
    parser = Parser(input("Enter a string to lex: "))
    parser.parse()
