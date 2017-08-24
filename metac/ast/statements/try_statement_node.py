from ..statement_node import StatementNode, Node

class CatchClauseNode(Node):
    def __init__(self, type_expr, except_id, block):
        self.type = type_expr
        self.id = except_id
        self.block = block

        self.scope = None

class TryStatementNode(StatementNode):
    def __init__(self, try_block, catch_clauses, default_catch):
        self.try_block = try_block
        self.catch_clauses = catch_clauses
        self.default_catch = default_catch

class ThrowStatementNode(StatementNode):
    def __init__(self, expr):
        self.expr = expr
