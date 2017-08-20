import unittest

from ..err import ReturnTypeMismatch

from .utils import run_test

class MiscTests(unittest.TestCase):
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

    def test_ref_and_deref(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    value: 45
                    ptr: *int(&value)

                    if value != *ptr
                        return 1

                    return 0

                return test()
                """
            )
        )

    def test_array(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    value: [4]int()

                    value[0] = 123
                    value[1] = 321
                    value[2] = 98
                    value[3] = 1

                    if value[0] != 123
                        return 1
                    if value[1] != 321
                        return 2
                    if value[2] != 98
                        return 3
                    if value[3] != 1
                        return 4

                    for i: 0 while i < 4
                        value[i] = 12
                    then i++

                    if value[0] != 12
                        return 5
                    if value[1] != 12
                        return 6
                    if value[2] != 12
                        return 7
                    if value[3] != 12
                        return 8

                    return 0

                return test()
                """
            )
        )

    def test_ptr_arithmetic(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    array: [3]int()

                    array[0] = 54
                    array[1] = 43
                    array[2] = 98

                    ptr: array as *int

                    if *(ptr + 0) != 54
                        return 1
                    elif *(ptr + 1) != 43
                        return 2
                    elif *(2 + ptr) != 98
                        return 3

                    ptr += 2

                    if *(ptr - 0) != 98
                        return 4
                    elif *(ptr - 1) != 43
                        return 5
                    elif *(ptr - 2) != 54
                        return 6

                    return 0

                return test()
                """
            )
        )
