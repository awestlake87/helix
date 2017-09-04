
from ..expr_node import ExprNode, UnaryNode, BinaryNode

class PtrExprNode(UnaryNode):
    pass

class RefExprNode(UnaryNode):
    pass

class DotExprNode(BinaryNode):
    pass

class IndexExprNode(BinaryNode):
    pass


class AsNode(BinaryNode):
    pass

class CastNode(BinaryNode):
    pass

class BitcastNode(BinaryNode):
    pass


class SizeofNode(UnaryNode):
    pass

class OffsetofNode(BinaryNode):
    pass

class TypeofNode(UnaryNode):
    pass

class InitNode(BinaryNode):
    pass

class AssignNode(BinaryNode):
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
