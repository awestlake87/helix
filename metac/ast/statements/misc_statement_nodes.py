from ..statement_node import StatementNode

class ReturnNode(StatementNode):
    def __init__(self, expr):
        self.expr = expr

class BreakNode(StatementNode):
    pass

class ContinueNode(StatementNode):
    pass
