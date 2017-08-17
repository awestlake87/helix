import unittest

from .utils import run_test

class DepTests(unittest.TestCase):
    def test_unit(self):
        run_test(
            """
            struct Blargh
                int @n

            extern fun int c()
                struct Lalala
                    Blargh @b

                ladeeda: Lalala()

                blargh: Blargh()
                blargh.n = 456

                return b(blargh)


            extern fun int b(Blargh blargh)
                return blargh.n

            return c()
            """
        )
