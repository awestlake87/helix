from ..statement_node import StatementNode

class ReturnNode(StatementNode):
    def __init__(self, expr):
        self.expr = expr
