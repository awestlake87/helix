
import unittest

from ..err import Todo

from .utils import run_test

class OwnershipTests(unittest.TestCase):
    def test_immutability(self):
        #with self.assertRaises(Todo):
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
