from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode

class AddNode(BinaryExprNode):
    pass

class SubNode(BinaryExprNode):
    pass

class MulNode(BinaryExprNode):
    pass

class DivNode(BinaryExprNode):
    pass

class ModExprNode(BinaryExprNode):
    pass


class AddAssignNode(BinaryExprNode):
    pass

class SubAssignNode(BinaryExprNode):
    pass

class MulAssignNode(BinaryExprNode):
    pass

class DivAssignNode(BinaryExprNode):
    pass

class ModAssignNode(BinaryExprNode):
    pass


class PreIncExprNode(UnaryExprNode):
    pass

class PostIncExprNode(UnaryExprNode):
    pass

class PreDecExprNode(UnaryExprNode):
    pass

class PostDecExprNode(UnaryExprNode):
    pass


class NegExprNode(UnaryExprNode):
    pass
