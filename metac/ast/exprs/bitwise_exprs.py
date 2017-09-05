from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode
from .misc_exprs import AssignNode

class BitAndNode(BinaryExprNode):
    pass

class BitXorNode(BinaryExprNode):
    pass

class BitOrNode(BinaryExprNode):
    pass

class BitNotNode(UnaryExprNode):
    pass

class BitShrNode(BinaryExprNode):
    pass

class BitShlNode(BinaryExprNode):
    pass


class BitAndAssignNode(AssignNode):
    pass

class BitXorAssignNode(AssignNode):
    pass

class BitOrAssignNode(AssignNode):
    pass

class BitShrAssignNode(AssignNode):
    pass

class BitShlAssignNode(AssignNode):
    pass
