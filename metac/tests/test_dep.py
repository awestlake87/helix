
import unittest

from ..lang import Parser
from ..dep import hoist, Scope, create_jit_target

def parse_ast(code):
    parser = Parser(code)
    return parser.parse()

class DepTests(unittest.TestCase):
    def test_unit(self):
        unit_ast = parse_ast(
            """
            struct Blargh
                int @n

            extern fun int c()
                struct Lalala
                    Blargh @b

                ladeeda: Lalala()

                blargh: Blargh()
                blargh.n = 456

                return b()


            extern fun int b()
                blargh: Blargh()
                blargh.n = 456

                return 0

            c()
            b()
            """
        )

        global_scope = Scope()

        hoist(global_scope, unit_ast)
        jit_target = create_jit_target(global_scope, unit_ast)

        jit_target.build()
