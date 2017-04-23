import unittest

from ..utils import run_test

class BitwiseExprTests(unittest.TestCase):
    def test_and(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    a: 0b1010
                    b: 0b1111
                    c: 0b0101

                    if a & 0b0101 != 0b0000
                        return 1

                    if b & 0b1010 != 0b1010
                        return 2

                    if c & 0b0101 != 0b0101
                        return 3


                    if a &= 0b0101 != 0b0000
                        return 4
                    elif a != 0b0000
                        return 5

                    if b &= 0b1010 != 0b1010
                        return 6
                    elif b != 0b1010
                        return 7

                    if c &= 0b0101 != 0b0101
                        return 8
                    elif c &= 0b0101 != 0b0101
                        return 9

                    return 0
                """
            )
        )

    def test_xor(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    a: 0b1010
                    b: 0b1111
                    c: 0b0101

                    if a ^ 0b0101 != 0b1111
                        return 1

                    if b ^ 0b1010 != 0b0101
                        return 2

                    if c ^ 0b0101 != 0b0000
                        return 3


                    if a ^= 0b0101 != 0b1111
                        return 4
                    elif a != 0b1111
                        return 5

                    if b ^= 0b1010 != 0b0101
                        return 6
                    elif b != 0b0101
                        return 7

                    if c ^= 0b0101 != 0b0000
                        return 8
                    elif c != 0b0000
                        return 9

                    return 0
                """
            )
        )

    def test_or(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    a: 0b1010
                    b: 0b1111
                    c: 0b0101

                    if a | 0b0101 != 0b1111
                        return 1

                    if b | 0b1010 != 0b1111
                        return 2

                    if c | 0b0101 != 0b0101
                        return 3


                    if a |= 0b0101 != 0b1111
                        return 4
                    elif a != 0b1111
                        return 5

                    if b |= 0b1010 != 0b1111
                        return 6
                    elif b != 0b1111
                        return 7

                    if c |= 0b0101 != 0b0101
                        return 8
                    elif c != 0b0101
                        return 9

                    return 0
                """
            )
        )

    def test_not(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    a: byte(0b10101010)
                    b: byte(0b00001111)
                    c: byte(0b01010101)

                    if ~a != 0b01010101
                        return 1

                    if ~b != 0b11110000
                        return 2

                    if ~c != 0b10101010
                        return 3

                    return 0
                """
            )
        )

    def test_shr(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    a: byte(0b10101010)
                    b: byte(0b00001111)
                    c: byte(0b01010101)

                    if a >> 4 != 0b11111010
                        return 1

                    if b >> 4 != 0b00000000
                        return 2

                    if c >> 4 != 0b00000101
                        return 3


                    if a >>= 3 != 0b11110101
                        return 4
                    elif a != 0b11110101
                        return 5


                    if b >>= 2 != 0b00000011
                        return 6
                    elif b != 0b00000011
                        return 7


                    if c >>= 6 != 0b00000001
                        return 8
                    elif c != 0b00000001
                        return 9

                    return 0
                """
            )
        )

    def test_shl(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test()
                    a: byte(0b10101010)
                    b: byte(0b00001111)
                    c: byte(0b01010101)

                    if a << 4 != 0b10100000
                        return 1

                    if b << 4 != 0b11110000
                        return 2

                    if c << 4 != 0b01010000
                        return 3


                    if a <<= 3 != 0b01010000
                        return 4
                    elif a != 0b01010000
                        return 5


                    if b <<= 2 != 0b00111100
                        return 6
                    elif b != 0b00111100
                        return 7


                    if c <<= 6 != 0b01000000
                        return 8
                    elif c != 0b01000000
                        return 9

                    return 0
                """
            )
        )
