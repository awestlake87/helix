
from ctypes import CFUNCTYPE, c_int

from ..compiler import Compiler


def compile_test(code):
    compiler = Compiler()
    return compiler.compile_unit(code)

def run_test(code):
    compiler = Compiler()

    unit = compiler.compile_unit(code)

    test = compiler.get_function(CFUNCTYPE(c_int), "test")

    return test()
