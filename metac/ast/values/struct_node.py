from ..expr_node import ExprNode

class StructNode(ExprNode):
    def __init__(self, id, attrs = [ ]):
        self.id = id
        self.attrs = attrs
