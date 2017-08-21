import unittest

from .utils import run_test

class DepTests(unittest.TestCase):
    def test_unit(self):
        self.assertEqual(
            456,
            run_test(
                """
                struct Blargh
                    int @n

                cfun int c()
                    struct Lalala
                        Blargh @b

                    ladeeda: Lalala()

                    blargh: Blargh()
                    blargh.n = 456

                    return b(blargh)


                cfun int b(Blargh blargh)
                    return blargh.n

                return c()
                """
            )
        )

    def test_circular_funs(self):
        self.assertEqual(
            0,
            run_test(
                """
                cfun int a(int n)
                    if n > 0
                        return b(n - 1)
                    else
                        return 0

                cfun int b(int n)
                    if n > 0
                        return a(n - 1)
                    else
                        return 0

                return a(15)
                """
            )
        )
