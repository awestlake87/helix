from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode
from .misc_exprs import AssignExprNode

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


class BitAndAssignExprNode(AssignExprNode):
    pass

class BitXorAssignExprNode(AssignExprNode):
    pass

class BitOrAssignExprNode(AssignExprNode):
    pass

class BitShrAssignExprNode(AssignExprNode):
    pass

class BitShlAssignExprNode(AssignExprNode):
    pass
