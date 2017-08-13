from .expr_node import BinaryExprNode, UnaryExprNode

class AndNode(BinaryExprNode):
    pass

class XorNode(BinaryExprNode):
    pass

class OrNode(BinaryExprNode):
    pass

class NotNode(UnaryExprNode):
    pass


class LtnExprNode(BinaryExprNode):
    pass

class GtnExprNode(BinaryExprNode):
    pass

class LeqExprNode(BinaryExprNode):
    pass

class GeqExprNode(BinaryExprNode):
    pass


class EqNode(BinaryExprNode):
    pass

class NeqNode(BinaryExprNode):
    pass
