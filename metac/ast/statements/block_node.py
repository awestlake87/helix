from ..statement_node import StatementNode

class BlockNode(StatementNode):
    def __init__(self, statements=[ ]):
        self.statements = statements

        self.scope = None
