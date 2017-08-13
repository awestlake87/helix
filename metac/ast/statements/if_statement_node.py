from ..statement_node import StatementNode

class IfStatementNode(StatementNode):
    def __init__(self, if_branches, else_block=None):
        self.if_branches = if_branches
        self.else_block = else_block
