from .expr_node import BinaryNode, UnaryNode

class AndNode(BinaryNode):
    pass

class XorNode(BinaryNode):
    pass

class OrNode(BinaryNode):
    pass

class NotNode(UnaryNode):
    pass


class LtnNode(BinaryNode):
    pass

class GtnNode(BinaryNode):
    pass

class LeqNode(BinaryNode):
    pass

class GeqNode(BinaryNode):
    pass


class EqlNode(BinaryNode):
    pass

class NeqNode(BinaryNode):
    pass
