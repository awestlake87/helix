from ..expr_node import ExprNode

class DataAttr(ExprNode):
    def __init__(self, type_expr, id):
        self.type = type_expr
        self.id = id

class StructNode(ExprNode):
    def __init__(self, id, attrs = [ ]):
        self.id = id
        self.attrs = attrs
