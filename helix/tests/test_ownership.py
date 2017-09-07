
import unittest

from ..err import Todo

from .utils import run_test

class OwnershipTests(unittest.TestCase):
    @unittest.SkipTest
    def test_immutability(self):
        with self.assertRaises(Todo):
            run_test(
                """
                a: 34
                a = 43

                return 0
                """
            )
