
import unittest

from metac import Compiler
from metac.err import ReturnTypeMismatch

from ctypes import CFUNCTYPE, c_int

class CompileTests(unittest.TestCase):
    def setUp(self):
        self._compiler = Compiler()

    def test_nested_fun(self):
        self._compiler.compile_unit(
            """
            extern fun int main(int argc, **char argv)
                intern fun int blargh(int a, int b)
                    return 0
                return 0
            """
        )

    def test_ptr_type(self):
        self._compiler.compile_unit(
            """
            intern fun *int omg()
                return nil
            intern fun ****int int_ptr_ptr_ptr_ptr()
                return nil
            """
        )

    def test_int_types(self):
        self._compiler.compile_unit(
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
            self._compiler.compile_unit(
                """
                intern fun *int ptr()
                    return 0
                """
            )

class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self._compiler = Compiler()

    def test_return_0(self):
        unit = self._compiler.compile_unit(
            """
            extern fun int return_0()
                return 0
            """
        )

        return_0 = self._compiler.get_function(CFUNCTYPE(c_int), "return_0")
        self.assertEqual(0, return_0())


    def test_return_arg(self):
        unit = self._compiler.compile_unit(
            """
            extern fun int return_arg(int arg)
                return arg
            """
        )

        return_arg = self._compiler.get_function(
            CFUNCTYPE(c_int, c_int), "return_arg"
        )
        self.assertEqual(4123, return_arg(4123))

    def test_fun_calls(self):
        unit = self._compiler.compile_unit(
            """
            intern fun int return_43(int a, int b)
                return 43
            extern fun int return_call(int a, int b)
                intern fun int call_fun(int a, int b)
                    return return_43(a, b)

                return call_fun(a, b)
            """
        )

        return_call = self._compiler.get_function(
            CFUNCTYPE(c_int, c_int, c_int), "return_call"
        )
        self.assertEqual(43, return_call(32, 44))

    def test_int_inits(self):
        unit = self._compiler.compile_unit(
            """
            extern fun int omg(int blargh)
                return int(blargh)
            """
        )

        int_inits = self._compiler.get_function(
            CFUNCTYPE(c_int, c_int), "omg"
        )

        self.assertEqual(123, int_inits(123))

        with self.assertRaises(ReturnTypeMismatch):
            self._compiler.compile_unit(
                """
                extern fun int omg()
                    return short(123)
                """
            )

    def test_if_statement(self):
        unit = self._compiler.compile_unit(
            """
            extern fun int test()
                if true
                    if false
                        return 2
                    else
                        if false
                            return 3
                        elif true
                            return 0
                        else
                            return 4

                return 1
            """
        )

        test = self._compiler.get_function(CFUNCTYPE(c_int), "test")
        self.assertEqual(0, test())


    def test_switch_statement(self):
        unit = self._compiler.compile_unit(
            """
            extern fun int test()
                switch 6
                    case 1
                        return 1

                    case 6
                        switch 4
                            case 5
                                return 2

                            default
                                return 0
                    case 5
                        return 3

                    default
                        return 4
            """
        )

        test = self._compiler.get_function(CFUNCTYPE(c_int), "test")
        self.assertEqual(0, test())

    def test_init(self):
        unit = self._compiler.compile_unit(
            """
            extern fun int test(int arg)
                a: b: arg
                return a
            """
        )

        test = self._compiler.get_function(CFUNCTYPE(c_int, c_int), "test")
        self.assertEqual(1234, test(1234))

if __name__ == "__main__":
    Compiler.initialize()
    unittest.main()
