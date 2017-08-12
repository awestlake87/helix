import unittest

from ...err import ReturnTypeMismatch

from ..utils import run_test, compile_test

class MiscExprTests(unittest.TestCase):

    @unittest.SkipTest
    def test_fun_calls(self):
        self.assertEqual(
            43,
            run_test(
                """
                extern fun int test()
                    extern fun int call_fun(int a, int b)
                        return return_43(a, b)

                    return call_fun(46, 3)

                extern fun int return_43(int a, int b)
                    return 43
                """
            )
        )

    @unittest.SkipTest
    def test_int_inits(self):
        self.assertEqual(
            123,
            run_test(
                """
                extern fun int test()
                    return int(123)
                """
            )
        )

        with self.assertRaises(ReturnTypeMismatch):
            compile_test(
                """
                extern fun int omg()
                    return short(123)
                """
            )

    @unittest.SkipTest
    def test_init(self):
        self.assertEqual(
            1234,
            run_test(
                """
                extern fun int test()
                    a: b: 1234
                    return a
                """
            )
        )

    @unittest.SkipTest
    def test_ternary_conditional(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    a: 432 if true else 321

                    if a == 321
                        return 1

                    a = 11 if false else 13

                    if a == 11
                        return 2

                    return 0
                """
            )
        )

    @unittest.SkipTest
    def test_structs(self):
        self.assertEqual(
            0,
            run_test(
                """
                struct Lard
                    int @fat

                struct Blargh
                    int @an_attr
                    int @_b123_b
                    Lard @_lard

                extern fun int test()
                    blargh: Blargh()

                    blargh.an_attr = 1
                    blargh._b123_b = 2
                    blargh._lard.fat = 5

                    if blargh.an_attr != 1
                        return 1

                    if blargh._b123_b != 2
                        return 2

                    if blargh._lard.fat != 5
                        return 3

                    return 0
                """
            )
        )
