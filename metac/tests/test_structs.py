import unittest

from .utils import run_test

class TestStructs(unittest.TestCase):

    def test_attr_funs(self):
        self.assertEqual(
            0,
            run_test(
                """
                struct Object
                    int @a

                    fun void @set_a(int val)
                        @a = val
                        return

                obj: Object()

                obj.a = 4
                obj.set_a(12)

                if obj.a != 12
                    return 1

                return 0
                """
            )
        )

    def test_attr_fun_uniqueness(self):
        self.assertEqual(
            0,
            run_test(
                """
                struct Object
                    fun int @do_something(int a)
                        return a

                fun int do_something(int a)
                    return 1

                obj: Object()

                if obj.do_something(43) != 43
                    return 1

                if do_something(12) != 1
                    return 2

                return 0
                """
            )
        )

    def test_nested_structs(self):
        self.assertEqual(
            0,
            run_test(
                """
                struct A
                    fun int @do_it()
                        return 568

                struct B
                    A @a

                    fun int @tell_a_to_do_it()
                        return @a.do_it()

                a: A()
                b: B()

                if a.do_it() != 568
                    return 1

                if b.a.do_it() != 568
                    return 2

                if b.tell_a_to_do_it() != 568
                    return 3

                return 0
                """
            )
        )
