import unittest

from .utils import run_test

class TestGlobals(unittest.TestCase):
    def test_global(self):
        self.assertEqual(
            0,
            run_test(
                """
                global int a_global: 45

                fun void set_a_global(int value)
                    a_global = value
                    return

                if a_global != 45
                    return 1

                set_a_global(128)

                if a_global != 128
                    return 2

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

                    fun void @set_value(int value)
                        @value = value
                        return

                fun void set_value(int value)
                    global_obj.set_value(value)
                    return

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
