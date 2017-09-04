
class BlockNode:
    def __init__(self, statements=[ ]):
        self.statements = statements

        self.scope = None

class IfNode:
    def __init__(self, if_branches, else_block=None):
        self.if_branches = if_branches
        self.else_block = else_block

        self.scope = None

class LoopNode:
    def __init__(
        self,
        for_clause,
        each_clause,
        while_clause,
        loop_body,
        then_clause,
        until_clause
    ):
        self.for_clause = for_clause
        self.each_clause = each_clause
        self.while_clause = while_clause
        self.loop_body = loop_body
        self.then_clause = then_clause
        self.until_clause = until_clause

        self.scope = None

class SwitchNode:
    def __init__(self, value, case_branches = [ ], default_block = None):
        self.value = value
        self.case_branches = case_branches
        self.default_block = default_block

        self.scope = None

class CatchNode:
    def __init__(self, type_expr, except_id, block):
        self.type = type_expr
        self.id = except_id
        self.block = block

        self.scope = None

class TryNode:
    def __init__(self, try_block, catch_clauses, default_catch):
        self.try_block = try_block
        self.catch_clauses = catch_clauses
        self.default_catch = default_catch

class ThrowNode:
    def __init__(self, expr):
        self.expr = expr


class ReturnNode:
    def __init__(self, expr = None):
        self.expr = expr

class BreakNode:
    pass

class ContinueNode:
    pass
