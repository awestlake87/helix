from ...err import Todo

from ..scope import Scope
from ..manglers import OperName

from .fun_sym import AttrFunSym

class ConstructOperSym(AttrFunSym):
    def __init__(self, unit, struct, ast, parent_scope):
        super().__init__(
            unit, struct, OperName(OperName.OP_CONSTRUCT), ast, parent_scope
        )

class DestructOperSym(AttrFunSym):
    def __init__(self, unit, struct, ast, parent_scope):
        super().__init__(
            unit, struct, OperName(OperName.OP_DESTRUCT), ast, parent_scope
        )
