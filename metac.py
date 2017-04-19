#!/usr/bin/python3

from metapy.lang import Parser

from metapy.ir import Module
from metapy.err import Todo

from ctypes import CFUNCTYPE, c_double
from metapy import Compiler

llvm_ir = """
   ; ModuleID = "examples/ir_fpadd.py"
   target triple = "unknown-unknown-unknown"
   target datalayout = ""

   define double @"fpadd"(double %".1", double %".2")
   {
   entry:
     %"res" = fadd double %".1", %".2"
     ret double %"res"
   }
   """

if __name__ == "__main__":
    Compiler.initialize()

    compiler = Compiler()

    compiler.compile_ir(llvm_ir)

    cfunc = compiler.get_function(
        CFUNCTYPE(c_double, c_double, c_double), "fpadd"
    )

    res = cfunc(1.0, 3.5)
    print("fpadd(...) = ", res)
