

from ...scope import Scope

class BlockSym:
    def __init__(self, parent_scope = None):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.statements = [ ]

class ReturnSym:
    def __init__(self, expr_sym):
        self.expr = expr_sym


class IfSym:
    def __init__(self, parent_scope):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.if_branches = [ ]
        self.else_block = None

class LoopSym:
    def __init__(self, parent_scope):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.for_clause = None
        self.each_clause = None
        self.while_clause = None
        self.loop_body = None
        self.then_clause = None
        self.until_clause = None

class SwitchSym:
    def __init__(self, parent_scope):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.value = None
        self.case_branches = [ ]
        self.default_block = None
