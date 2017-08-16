from contextlib import contextmanager

import llvmlite.binding as binding

from ..scope import Scope
from ..target import Target
from .fun_symbol import FunSymbol

from ...ir import UnitValue
from ...ast import *

from ..hoist import hoist_block
from ..get_deps import get_block_deps

class UnitTarget(Target):
    def __init__(self, symbol, on_llvm_module=lambda m: None):
        self.symbol = symbol
        self._on_llvm_module = on_llvm_module

        super().__init__(
            [ self.symbol._jit_fun.get_target() ] + get_block_deps(self.symbol, self.symbol.ast)
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

class UnitSymbol:
    def __init__(self, id, ast):
        self.ast = ast
        self.scope = Scope()

        self.id = id
        self.ir_value = UnitValue(self.id)

        hoist_block(self, self.ast)

        self._jit_fun = FunSymbol(
            self,
            FunNode(
                FunTypeNode(IntTypeNode(32, True), [ ]),
                "__jit__",
                [ ],
                self.ast
            ),
            self.scope
        )

        self._target = None
        self._llvm_module = None

    def _on_llvm_module(self, module):
        self._llvm_module = module

    def get_target(self):
        if self._target is None:
            self._target = UnitTarget(
                self, on_llvm_module=self._on_llvm_module
            )

        return self._target

    def get_llvm_module(self):
        return self._llvm_module

    def get_ir_value(self):
        return self.ir_value

    @contextmanager
    def use_scope(self, scope):
        assert not scope is None

        old_scope = self.scope
        self.scope = scope

        yield

        self.scope = old_scope
