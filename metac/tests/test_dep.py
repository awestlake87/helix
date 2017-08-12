
import unittest

from ..lang import Parser
from ..dep import ModuleSymbol, Scope

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

            extern fun int c()
                struct Lalala
                    Blargh @b

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
        global_scope = Scope()

        module_symbol = ModuleSymbol("test", global_scope)
        global_scope.insert("test", module_symbol)

        module_symbol.set_entry(block)

        module_symbol.get_target().meet()
