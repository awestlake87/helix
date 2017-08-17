
from ..expr_node import ExprNode

class FunNode(ExprNode):
    def __init__(self, type, id, param_ids, body):
        self.type = type
        self.id = id
        self.param_ids = param_ids
        self.body = body
