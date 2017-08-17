import llvmlite.binding as binding

from .target import Target

from .gen_deps import gen_block_deps

class UnitTarget(Target):
    def __init__(self, symbol, on_llvm_module=lambda m: None):
        self.symbol = symbol
        self._on_llvm_module = on_llvm_module

        super().__init__(
            [ self.symbol._jit_fun.get_target() ] + 
            gen_block_deps(self.symbol, self.symbol.ast)
        )

    def _build_target(self):
        try:
            llvm_module = binding.parse_assembly(
                str(self.symbol.get_ir_value().get_llvm_value())
            )

            llvm_module.verify()

            self._on_llvm_module(llvm_module)

        except Exception as e:
            print(e)
            print(self.symbol.get_ir_value().get_llvm_value())
