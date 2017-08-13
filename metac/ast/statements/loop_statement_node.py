from ..statement_node import StatementNode

class LoopStatementNode(StatementNode):
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
