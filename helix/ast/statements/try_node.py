from ..statement_node import StatementNode, Node

class CatchNode(Node):
    def __init__(self, type_expr, except_id, block):
        self.type = type_expr
        self.id = except_id
        self.block = block

        self.scope = None

class TryNode(StatementNode):
    def __init__(self, try_block, catch_clauses, default_catch):
        self.try_block = try_block
        self.catch_clauses = catch_clauses
        self.default_catch = default_catch

class ThrowNode(StatementNode):
    def __init__(self, expr):
        self.expr = expr
