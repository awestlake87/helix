from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode

class AddExprNode(BinaryExprNode):
    pass

class SubExprNode(BinaryExprNode):
    pass

class MulExprNode(BinaryExprNode):
    pass

class DivExprNode(BinaryExprNode):
    pass

class ModExprNode(BinaryExprNode):
    pass


class AddAssignExprNode(BinaryExprNode):
    pass

class SubAssignExprNode(BinaryExprNode):
    pass

class MulAssignExprNode(BinaryExprNode):
    pass

class DivAssignExprNode(BinaryExprNode):
    pass

class ModAssignExprNode(BinaryExprNode):
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
