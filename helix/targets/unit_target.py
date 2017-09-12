from contextlib import contextmanager
from llvmlite import binding

from ..err import Todo

from .target import Target

class UnitTarget(Target):
    def __init__(self, symbol, on_llvm_module=lambda m: None):
        super().__init__([ ])

        self.symbol = symbol
        self._on_llvm_module = on_llvm_module

    def build(self):
        try:
            llvm_module = binding.parse_assembly(
                str(self.symbol.ir_value.get_llvm_value())
            )

            llvm_module.verify()

            self._on_llvm_module(llvm_module)

        except Exception as e:
            print(e)
            print(self.symbol.ir_value.get_llvm_value())

            raise e
