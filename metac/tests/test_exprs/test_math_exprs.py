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

                return test()
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

                return test()
                """
            )
        )

    def test_add(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    if 2 + 2 != 4
                        return 1

                    if -2 + 3 != 1
                        return 2

                    if 2 + -3 != -1
                        return 3

                    a: 4
                    b: 4

                    if a + b != 8
                        return 4

                    a += 5

                    if a != 9
                        return 5

                    b += -5

                    if b != -1
                        return 6


                    return 0

                return test()
                """
            )
        )

    def test_sub(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    if -2 - -2 != 0
                        return 1

                    if -2 - 3 != -5
                        return 2

                    if 2 - -3 != 5
                        return 3

                    a: 4
                    b: 4

                    if a - b != 0
                        return 4

                    a -= 5

                    if a != -1
                        return 5

                    b -= -5

                    if b != 9
                        return 6


                    return 0

                return test()
                """
            )
        )

    def test_mul(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    if 2 * 2 != 4
                        return 1

                    if -2 * 3 != -6
                        return 2

                    if 2 * -3 != -6
                        return 3

                    a: 4
                    b: 4

                    if a * b != 16
                        return 4

                    a *= 5

                    if a != 20
                        return 5

                    b *= -5

                    if b != -20
                        return 6


                    return 0

                return test()
                """
            )
        )

    def test_sdiv(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    if 2 / 2 != 1
                        return 1

                    if -2 / 3 != 0
                        return 2

                    if 6 / -3 != -2
                        return 3

                    a: 21
                    b: 2

                    if a / b != 10
                        return 4

                    a /= 5

                    if a != 4
                        return 5

                    b /= -1

                    if b != -2
                        return 6


                    return 0

                return test()
                """
            )
        )

    def test_smod(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    if 2 % 2 != 0
                        return 1

                    if -2 % 3 != -2
                        return 2

                    if 7 % -3 != 1
                        return 3

                    a: 21
                    b: 2

                    if a % b != 1
                        return 4

                    a %= 5

                    if a != 1
                        return 5

                    b %= -3

                    if b != 2
                        return 6


                    return 0

                return test()
                """
            )
        )
