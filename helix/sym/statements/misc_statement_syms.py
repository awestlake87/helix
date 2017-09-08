
from ..scope import *

class BlockSym:
    def __init__(self, parent_scope):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.statements = [ ]

class ReturnSym:
    def __init__(self, expr = None):
        self.expr = expr

class IfSym:
    def __init__(self, parent_scope, if_branches, else_block):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.if_branches = if_branches
        self.else_block = else_block

class LoopSym:
    def __init__(
        self,
        parent_scope,
        for_clause,
        each_clause,
        while_clause,
        loop_body,
        then_clause,
        until_clause
    ):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.for_clause = for_clause
        self.each_clause = each_clause
        self.while_clause = while_clause
        self.loop_body = loop_body
        self.then_clause = then_clause
        self.until_clause = until_clause

class SwitchSym:
    def __init__(
        self, parent_scope, value, case_branches = [ ], default_block = None
    ):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.value = value
        self.case_branches = case_branches
        self.default_block = default_block

class TrySym:
    def __init__(self, parent_scope, try_block, catch_clauses, default_catch):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)

        self.try_block = try_block
        self.catch_clauses = catch_clauses
        self.default_catch = default_catch

class CatchSym:
    def __init__(self, type_expr, except_id, block):
        self.type = type_expr
        self.id = except_id
        self.block = block

        self.scope = None

class ThrowSym:
    def __init__(self, expr):
        self.expr = expr

class BreakSym:
    pass

class ContinueSym:
    pass
