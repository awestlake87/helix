
import unittest

from ..lang import Parser
from ..dep import UnitSymbol

def parse_ast(code):
    parser = Parser(code)
    return parser.parse()

class DepTests(unittest.TestCase):
    def test_unit(self):
        block = parse_ast(
            """
            struct Blargh
                int @n

            fun int a(Blargh blargh)
                return blargh.n

            fun int a()
                return 123

            intern fun int c()
                struct Lalala
                    Blargh @a

                ladeeda: Lalala()

                blargh: Blargh()
                blargh.n = 456

                if a() != 123
                    return 1

                elif a(blargh) != 456
                    return 2

            extern fun int b()
                blargh: Blargh()
                blargh.n = 456

                if a() != 123
                    return 1

                elif a(blargh) != 456
                    return 2

                return 0
            """
        )

        unit_symbol = UnitSymbol("test", block)

        print(unit_symbol.get_target())

        unit_symbol.get_target().build()
