from ctypes import CFUNCTYPE, c_int

import llvmlite.binding as binding

from .target import Target

from .manglers import mangle_name, OperName

class JitTarget(Target):
    def __init__(self, units):
        self.units = units

        self._llvm_target = binding.Target.from_default_triple()
        self._llvm_target_machine = self._llvm_target.create_target_machine()
        self._llvm_backing_module = binding.parse_assembly("")

        self._llvm_engine = binding.create_mcjit_compiler(
            self._llvm_backing_module, self._llvm_target_machine
        )

        super().__init__([ unit.target for unit in units ])

        self._jit_fun = None

    def build(self):

        for unit in self.units:
            self._llvm_engine.add_module(unit.get_llvm_module())

        self._llvm_engine.finalize_object()

        self._jit_fun = CFUNCTYPE(c_int)(
            self._llvm_engine.get_function_address(
                mangle_name([ self.units[0].id, OperName(OperName.OP_JIT) ])
            )
        )

    def run(self):
        return self._jit_fun()
