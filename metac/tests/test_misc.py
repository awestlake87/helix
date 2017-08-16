import unittest

from ..err import ReturnTypeMismatch

from .utils import run_test

class MiscTests(unittest.TestCase):
    @unittest.SkipTest
    def test_nested_fun(self):
        self.assertEqual(
            5,
            run_test(
                """
                extern fun int test()
                    extern fun int blargh(int a, int b)
                        return 5
                    return blargh(1, 2)

                return test()
                """
            )
        )

    @unittest.SkipTest
    def test_ptr_type(self):
        run_test(
            """
            extern fun *int omg()
                return nil
            extern fun ****int int_ptr_ptr_ptr_ptr()
                return nil

            if int_ptr_ptr_ptr_ptr() != nil
                return 1

            elif omg() != nil
                return 2

            else
                return 0

            """
        )

    @unittest.SkipTest
    def test_int_types(self):
        run_test(
            """
            extern fun bit get_bit()
                return 0

            extern fun byte get_byte()
                return 0
            extern fun short get_short()
                return 0
            extern fun int get_int()
                return 0
            extern fun long get_long()
                return 0

            extern fun ubyte get_ubyte()
                return 0
            extern fun ushort get_ushort()
                return 0
            extern fun uint get_uint()
                return 0
            extern fun ulong get_ulong()
                return 0

            get_bit()
            get_byte()
            get_short()
            get_int()
            get_long()

            get_ubyte()
            get_ushort()
            get_uint()
            get_ulong()

            return 0
            """
        )

    @unittest.SkipTest
    def test_return_type_mismatch(self):
        with self.assertRaises(ReturnTypeMismatch):
            run_test(
                """
                extern fun *int ptr()
                    return 1

                ptr()
                return 0
                """
            )
