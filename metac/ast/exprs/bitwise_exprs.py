from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode

class BitAndExprNode(BinaryExprNode):
    pass

class BitXorExprNode(BinaryExprNode):
    pass

class BitOrExprNode(BinaryExprNode):
    pass

class BitNotExprNode(UnaryExprNode):
    pass

class BitShrExprNode(BinaryExprNode):
    pass

class BitShlExprNode(BinaryExprNode):
    pass


class BitAndAssignExprNode(BinaryExprNode):
    pass

class BitXorAssignExprNode(BinaryExprNode):
    pass

class BitOrAssignExprNode(BinaryExprNode):
    pass

class BitShrAssignExprNode(BinaryExprNode):
    pass

class BitShlAssignExprNode(BinaryExprNode):
    pass
