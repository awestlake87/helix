from ..err import Todo

from .fun_symbol import AttrFunSymbol

from .scope import Scope
from .manglers import OperName

class ConstructOperSymbol(AttrFunSymbol):
    def __init__(self, unit, struct, ast, parent_scope):
        super().__init__(
            unit, struct, OperName(OperName.OP_CONSTRUCT), ast, parent_scope
        )

class DestructOperSymbol(AttrFunSymbol):
    def __init__(self, unit, struct, ast, parent_scope):
        super().__init__(
            unit, struct, OperName(OperName.OP_DESTRUCT), ast, parent_scope
        )
