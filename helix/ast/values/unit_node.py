from ..expr_node import ExprNode

class UnitNode(ExprNode):
    def __init__(self, id, block):
        self.id = id
        self.block = block
