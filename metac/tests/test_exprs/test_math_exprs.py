import unittest

from ..utils import run_test

class MathExprTests(unittest.TestCase):
    def test_inc_and_dec(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    a: 0

                    b: a++

                    if a != 1
                        return 1

                    if b != 0
                        return 2

                    a--

                    if a != 0
                        return 3

                    b = --a

                    if a != -1
                        return 4

                    if b != -1
                        return 5

                    ++a

                    if a != 0
                        return 6

                    return 0
                """
            )
        )

    def test_negate(self):
        self.assertEqual(
            -143,
            run_test(
                """
                extern fun int test()
                    return -143
                """
            )
        )
