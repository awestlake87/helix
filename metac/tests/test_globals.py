import unittest

from .utils import run_test

class TestGlobals(unittest.TestCase):
    def test_global(self):
        self.assertEqual(
            0,
            run_test(
                """
                global int a_global: 45

                fun int set_a_global(int value)
                    a_global = value

                    return 0

                if a_global != 45
                    return 1

                if set_a_global(128) != 0
                    return 2

                if a_global != 128
                    return 3

                return 0
                """
            )
        )

    def test_global_struct(self):
        self.assertEqual(
            0,
            run_test(
                """
                global global_obj: Object()

                struct Object
                    int @value

                    fun int @set_value(int value)
                        @value = value
                        return 0

                fun int set_value(int value)
                    return global_obj.set_value(value)

                global_obj.value = 12

                if global_obj.value != 12
                    return 1

                set_value(43)

                if global_obj.value != 43
                    return 2

                return 0
                """
            )
        )
