
from ...scope import Scope

from ..expr_sym import ExprSym

class UnitSym(ExprSym):
    def __init__(self, parent_scope = None):
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)

        self.block = None
