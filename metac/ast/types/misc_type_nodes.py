from ..expr_node import ExprNode

class FunTypeNode(ExprNode):
    def __init__(self, ret_type, param_types):
        self.ret_type = ret_type
        self.param_types = param_types

class IntTypeNode(ExprNode):
    def __init__(self, num_bits, is_signed):
        self.num_bits = num_bits
        self.is_signed = is_signed
