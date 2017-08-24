import unittest

from .utils import run_test

class ExceptionTests(unittest.TestCase):
    def test_catch(self):
        self.assertEqual(
            0,
            run_test(
                """
                try
                    throw 13

                catch *int e
                    if *e != 13
                        return 1
                    else
                        return 0

                catch
                    return 1
                """
            )
        )

    def test_default_catch(self):
        self.assertEqual(
            0,
            run_test(
                """
                try
                    throw 123

                catch
                    return 0
                """
            )
        )

    def test_try_catch_continue(self):
        self.assertEqual(
            0,
            run_test(
                """
                try
                    for i: 0 while i < 5
                        if i == 4
                            throw i
                    then i++

                catch *int e
                    if *e != 4
                        return 1

                return 0
                """
            )
        )

    def test_multi_catch(self):
        self.assertEqual(
            0,
            run_test(
                """
                try
                    throw 12

                catch *byte e
                    return 1

                catch *int e
                    return 0

                catch
                    return 2
                """
            )
        )
