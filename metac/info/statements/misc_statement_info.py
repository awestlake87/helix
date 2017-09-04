
from ...scope import Scope

class BlockInfo:
    def __init__(self, parent_scope):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.statements = [ ]

class ReturnInfo:
    def __init__(self, expr):
        self.expr = expr

class IfInfo:
    def __init__(self, parent_scope):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.if_branches = [ ]
        self.else_block = None

class LoopInfo:
    def __init__(self, parent_scope):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.for_clause = None
        self.each_clause = None
        self.while_clause = None
        self.loop_body = None
        self.then_clause = None
        self.until_clause = None

class SwitchInfo:
    def __init__(self, parent_scope):
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)

        self.value = None
        self.case_branches = [ ]
        self.default_block = None

class TryInfo:
    pass

class ThrowInfo:
    pass

class BreakInfo:
    pass

class ContinueInfo:
    pass
