
import llvmlite.binding as llvm

from .lang import Parser
from .ir import Module
from .ast import UnitNode

class Compiler:
    @staticmethod
    def initialize():
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

    def __init__(self):
        self._target = llvm.Target.from_default_triple()
        self._target_machine = self._target.create_target_machine()
        self._backing_mod = llvm.parse_assembly("")

        self._engine = llvm.create_mcjit_compiler(
            self._backing_mod, self._target_machine
        )

    def compile_ir(self, llvm_ir):
        llvm_module = llvm.parse_assembly(llvm_ir)
        llvm_module.verify()

        self._engine.add_module(llvm_module)
        self._engine.finalize_object()

        return llvm_module

    def compile_unit(self, code, dump_ir=False):
        parser = Parser(code)
        ast = UnitNode("test", parser.parse())

        module = Module()
        unit = ast.gen_module_value(module)

        try:
            llvm_module = llvm.parse_assembly(str(unit._module))
            llvm_module.verify()

        except Exception as e:
            print(unit._module)
            raise e

        if dump_ir:
            print(unit._module)

        self._engine.add_module(llvm_module)
        self._engine.finalize_object()

        return llvm_module


    def get_function(self, type, name):
        fun_ptr = self._engine.get_function_address(name)

        return type(fun_ptr)
