

from ...scope import Scope

class BlockSym:
    def __init__(self, parent_scope = None):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.statements = [ ]
        
class ReturnSym:
    def __init__(self, expr_sym):
        self.expr = expr_sym
