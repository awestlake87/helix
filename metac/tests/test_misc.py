import unittest

from ..err import ReturnTypeMismatch

from .utils import run_test, compile_test

class MiscTests(unittest.TestCase):
    def test_nested_fun(self):
        self.assertEqual(
            5,
            run_test(
                """
                extern fun int test()
                    intern fun int blargh(int a, int b)
                        return 5
                    return blargh(1, 2)
                """
            )
        )

    def test_ptr_type(self):
        compile_test(
            """
            intern fun *int omg()
                return nil
            intern fun ****int int_ptr_ptr_ptr_ptr()
                return nil
            """
        )

    def test_int_types(self):
        compile_test(
            """
            intern fun bit get_bit()
                return 0

            intern fun byte get_byte()
                return 0
            intern fun short get_short()
                return 0
            intern fun int get_int()
                return 0
            intern fun long get_long()
                return 0

            intern fun ubyte get_ubyte()
                return 0
            intern fun ushort get_ushort()
                return 0
            intern fun uint get_uint()
                return 0
            intern fun ulong get_ulong()
                return 0
            """
        )

    def test_return_type_mismatch(self):
        with self.assertRaises(ReturnTypeMismatch):
            compile_test(
                """
                intern fun *int ptr()
                    return 0
                """
            )
