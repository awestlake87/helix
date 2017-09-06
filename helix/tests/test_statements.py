
import unittest

from .utils import run_test

class LoopTests(unittest.TestCase):

    def test_return(self):
        self.assertEqual(
            6573,
            run_test(
                """
                cfun int! test()
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
                val: 0

                for i: 0 while i < 10
                    val = i
                then i++

                return val
                """
            )
        )

    def test_while_loop(self):
        self.assertEqual(
            100,
            run_test(
                """
                i: 1000

                while i != 100
                    --i

                return i
                """
            )
        )

    def test_until_loop(self):
        self.assertEqual(
            100,
            run_test(
                """
                i: 0

                loop
                    ++i
                until i == 100

                return i
                """
            )
        )

    def test_switch(self):
        self.assertEqual(
            0,
            run_test(
                """
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
        )

    def test_multi_case_switch(self):
        self.assertEqual(
            0,
            run_test(
                """
                switch 3
                    case 0
                    case 1
                    case 2
                        return 1

                    case 3
                        switch 45
                            case 1
                            case 10
                            case 45
                            case 50
                                return 0

                            default
                                return 2

                    default
                        return 3
                """
            )
        )

    def test_if(self):
        self.assertEqual(
            0,
            run_test(
                """
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
        )

    def test_loop_control(self):
        self.assertEqual(
            0,
            run_test(
            """
            n: 0

            while n < 12
                if n == 7
                    break

            then n++

            if n != 7
                return 1

            for n = 0 while n < 10
                if n < 5
                    continue
                else
                    break
            then n++

            if n != 5
                return 2


            for n = 0 while n < 10
                for i: 0
                    if i == 10
                        break
                then i++
            then n++

            if n != 10
                return 3

            return 0
            """
            )
        )
