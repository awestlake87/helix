from .expr_node import BinaryExprNode, UnaryExprNode

class AndNode(BinaryExprNode):
    pass

class XorNode(BinaryExprNode):
    pass

class OrNode(BinaryExprNode):
    pass

class NotNode(UnaryExprNode):
    pass


class LtnNode(BinaryExprNode):
    pass

class GtnNode(BinaryExprNode):
    pass

class LeqNode(BinaryExprNode):
    pass

class GeqNode(BinaryExprNode):
    pass


class EqlNode(BinaryExprNode):
    pass

class NeqNode(BinaryExprNode):
    pass
