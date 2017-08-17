
import unittest

from .utils import run_test

class LoopTests(unittest.TestCase):
    def test_return(self):
        self.assertEqual(
            6573,
            run_test(
                """
                extern fun int test()
                    return 6573

                return test()
                """
            )
        )

    def test_for_loop(self):
        self.assertEqual(
            9,
            run_test(
                """
                extern fun int test()
                    val: 0

                    for i: 0 while i < 10
                        val = i
                    then i++

                    return val

                return test()
                """
            )
        )

    def test_while_loop(self):
        self.assertEqual(
            100,
            run_test(
                """
                extern fun int test()
                    i: 1000

                    while i != 100
                        --i

                    return i

                return test()
                """
            )
        )

    def test_until_loop(self):
        self.assertEqual(
            100,
            run_test(
                """
                extern fun int test()
                    i: 0

                    loop
                        ++i
                    until i == 100

                    return i

                return test()
                """
            )
        )

    def test_switch(self):
        self.assertEqual(
            0,
            run_test(
                """
                extern fun int test(int value)
                    switch value
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

                return test(6)
                """
            )
        )

    def test_if(self):
        self.assertEqual(
            0,
            run_test(
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

                return test()
                """
            )
        )
