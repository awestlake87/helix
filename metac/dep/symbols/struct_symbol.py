
from ..target import Target

from ..get_deps import get_expr_deps

class StructTarget(Target):
    def __init__(self, symbol):
        self.symbol = symbol

        deps = [ ]
        for attr_type, _ in self.symbol.ast.attrs:
            deps += get_expr_deps(self.symbol.parent_scope, attr_type)

        super().__init__(deps)

    def _build_target(self):
        print("build {}".format(self.symbol.ast.id))

class StructSymbol:
    def __init__(self, parent_scope, ast):
        self.parent_scope = parent_scope
        self.ast = ast

        self._target = None

    def get_target(self):
        if self._target is None:
            self._target = StructTarget(self)

        return self._target
