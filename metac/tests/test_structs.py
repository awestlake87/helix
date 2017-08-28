import unittest

from .utils import run_test

class TestStructs(unittest.TestCase):

    def test_attr_funs(self):
        self.assertEqual(
            0,
            run_test(
                """
                cfun int printf(*char fmt, vargs)

                struct Object
                    int @a

                    fun int @set_a(int val)
                        @a = val
                        return 0

                obj: Object()

                obj.a = 4
                obj.set_a(12)

                if obj.a != 12
                    return 1

                return 0
                """
            )
        )
