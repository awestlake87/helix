from ..expr_node import ExprNode

class UnitNode(ExprNode):
    def __init__(self, id, block):
        self.block = block
