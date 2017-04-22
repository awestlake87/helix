import unittest

from ..utils import run_test

class BitwiseExprTests(unittest.TestCase):
    def test_and(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    return 1
                """
            )
        )
