
from ...scope import Scope

class BlockInfo:
    def __init__(self, parent_scope):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.statements = [ ]

class ReturnInfo:
    def __init__(self, expr):
        self.expr = expr

class IfStatementInfo:
    pass

class LoopStatementInfo:
    pass

class SwitchStatementInfo:
    pass

class TryStatementInfo:
    pass

class ThrowStatementInfo:
    pass

class BreakInfo:
    pass

class ContinueInfo:
    pass
