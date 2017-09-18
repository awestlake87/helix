import unittest

from .utils import run_test

class ConditionTests(unittest.TestCase):
    def test_and(self):
        self.assertEqual(
            0,
            run_test(
                """
                if true and true
                    pass

                if true and false
                    return 1

                if false and true
                    return 2

                if false and false
                    return 3

                mut a: 123

                if false and a = 34
                    return 4

                else
                    if a == 34
                        return 5

                if true and a = 45
                    if a != 45
                        return 6

                return 0
                """
            )
        )

    def test_xor(self):
        self.assertEqual(
            0,
            run_test(
                """
                if true xor true
                    return 1

                if false xor true
                    pass

                if true xor false
                    pass

                if false xor false
                    return 2

                return 0
                """
            )
        )

    def test_or(self):
        self.assertEqual(
            0,
            run_test(
                """
                if true or true
                    pass

                if true or false
                    pass

                if false or true
                    pass

                if false or false
                    return 1

                mut a: 123

                if false or a = 34
                    if a == 34
                        pass
                    else
                        return 2

                if true or a = 45
                    if a == 45
                        return 3

                return 0
                """
            )
        )

    def test_not(self):
        self.assertEqual(
            0,
            run_test(
                """
                if not true
                    return 1

                if not not false
                    return 2

                if not false
                    pass

                return 0
                """
            )
        )
