import unittest

from ..err import ReturnTypeMismatch

from .utils import run_test

class MiscTests(unittest.TestCase):
    def test_nested_fun(self):
        self.assertEqual(
            5,
            run_test(
                """
                cfun int! test()
                    cfun int! blargh(int! a, int! b)
                        return 5
                    return blargh(1, 2)

                return test()
                """
            )
        )

    def test_ptr_type(self):
        self.assertEqual(
            0,
            run_test(
                """
                cfun *int! omg()
                    return nil
                cfun ****int! int_ptr_ptr_ptr_ptr()
                    return nil

                if int_ptr_ptr_ptr_ptr() != nil
                    return 1

                elif omg() != nil
                    return 2

                else
                    return 0

                """
            )
        )

    def test_int_types(self):
        self.assertEqual(
            0,
            run_test(
                """
                cfun bit! get_bit()
                    return 0

                cfun byte! get_byte()
                    return 0
                cfun short! get_short()
                    return 0
                cfun int! get_int()
                    return 0
                cfun long! get_long()
                    return 0

                cfun ubyte! get_ubyte()
                    return 0
                cfun ushort! get_ushort()
                    return 0
                cfun uint! get_uint()
                    return 0
                cfun ulong! get_ulong()
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
        )

    def test_return_type_mismatch(self):
        with self.assertRaises(ReturnTypeMismatch):
            run_test(
                """
                cfun *int! ptr()
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
                value: 45
                ptr: *int(&value)

                if value != *ptr
                    return 1

                return 0
                """
            )
        )

    def test_array(self):
        self.assertEqual(
            0,
            run_test(
                """
                mut value: [4]int()

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

                for mut i: 0 while i < 4
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
                """
            )
        )

    def test_ptr_arithmetic(self):
        self.assertEqual(
            0,
            run_test(
                """
                mut array: [3]int()

                array[0] = 54
                array[1] = 43
                array[2] = 98

                mut ptr: array as *int

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
                """
            )
        )

    def test_string(self):
        self.assertEqual(
            0,
            run_test(
                """
                str: "ab\\"c'\\n"

                if str[0] != 'a'
                    return 1
                if str[1] != 'b'
                    return 2
                if str[2] != '"'
                    return 3
                if str[3] != 'c'
                    return 4
                if str[4] != '\\''
                    return 5
                if str[5] != '\\n'
                    return 6
                if str[6] != 0
                    return 7

                return 0
                """
            )
        )

    def test_extern_symbol(self):
        self.assertEqual(
            0,
            run_test(
                """
                cfun uint! strlen(*char! s)

                s: "lol"

                if strlen(s) != 3
                    return 1
                elif strlen("hahhaa") != 6
                    return 2

                return 0
                """
            )
        )

    def test_vargs(self):
        self.assertEqual(
            0,
            run_test(
                """
                cfun int! printf(*char! format, vargs)
                cfun int! snprintf(*char! str, uint! n, *char! format, vargs)
                cfun int! strcmp(*char! a, *char! b)

                buffer: [50]char()
                value: int(45)

                snprintf(buffer, 50, "value: %d %s", value, "lol" as *char)

                if strcmp(buffer, "value: 45 lol") != 0
                    return 1

                return 0
                """
            )
        )

    def test_sizeof_offsetof(self):
        self.assertEqual(
            0,
            run_test(
                """
                struct Blargh
                    int<32> @a
                    int<32> @b

                if sizeof Blargh != 8
                    return 1

                if Blargh offsetof @a != 0
                    return 2

                if Blargh offsetof @b != 4
                    return 3

                blargh: Blargh()

                if sizeof blargh.a != 4
                    return 4

                return 0
                """
            )
        )
