
from ..scope import Scope
from ..target import Target

from ..get_deps import get_expr_deps, get_block_deps

class FunTarget(Target):
    def __init__(self, symbol):
        self.symbol = symbol

        deps = [ ]

        deps += get_expr_deps(self.symbol.parent_scope, self.symbol.ast.type)
        deps += get_block_deps(self.symbol.scope, self.symbol.ast.body)

        super().__init__(deps)

    def _build_target(self):
        print("build {}".format(self.symbol.ast.id))

class FunSymbol:
    def __init__(self, ast, parent_scope):
        super().__init__()

        self.ast = ast
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)

        self._target = None

    def get_target(self):
        if self._target is None:
            self._target = FunTarget(self)

        return self._target
