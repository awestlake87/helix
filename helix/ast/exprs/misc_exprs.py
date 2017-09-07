
from ..expr_node import ExprNode, UnaryExprNode, BinaryExprNode

class PtrNode(UnaryExprNode):
    pass

class RefNode(UnaryExprNode):
    pass

class MutNode(UnaryExprNode):
    pass

class DotNode(BinaryExprNode):
    pass

class IndexNode(BinaryExprNode):
    pass



class AsNode(BinaryExprNode):
    pass

class CastNode(BinaryExprNode):
    pass

class BitcastNode(BinaryExprNode):
    pass



class SizeofNode(UnaryExprNode):
    pass

class OffsetofNode(BinaryExprNode):
    pass

class TypeofNode(UnaryExprNode):
    pass

class InitNode(BinaryExprNode):
    pass

class AssignNode(BinaryExprNode):
    pass



class BangNode(UnaryExprNode):
    pass

class TropeNode(UnaryExprNode):
    pass



class CallNode(ExprNode):
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args

class EmbedCallNode(ExprNode):
    def __init__(self, lhs, args):
        self.lhs = lhs
        self.args = args


class TernaryConditionalNode(ExprNode):
    def __init__(self, lhs, condition, rhs):
        self.lhs = lhs
        self.condition = condition
        self.rhs = rhs
