
import unittest

from ..err import ValueIsNotMut

from .utils import run_test

class OwnershipTests(unittest.TestCase):
    def test_immutability(self):
        with self.assertRaises(ValueIsNotMut):
            self.assertEqual(
                0,
                run_test(
                    """
                    a: 34
                    a = 43

                    return 1
                    """
                )
            )

    def test_mutability(self):
        self.assertEqual(
            0,
            run_test(
                """
                mut a: 34
                a = 43

                if a != 43
                    return 1

                return 0
                """
            )
        )

    def test_transferability(self):
        with self.assertRaises(ValueIsNotMut):
            self.assertEqual(
                0,
                run_test(
                    """
                    mut a: 34
                    b: a

                    b = 34

                    return 1
                    """
                )
            )
