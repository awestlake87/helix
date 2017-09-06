from ..statement_node import StatementNode

class SwitchNode(StatementNode):
    def __init__(self, value, case_branches = [ ], default_block = None):
        self.value = value
        self.case_branches = case_branches
        self.default_block = default_block

        self.scope = None
