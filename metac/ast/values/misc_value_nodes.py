from ..expr_node import ExprNode

class LiteralNode(ExprNode):
    pass

class AutoIntNode(LiteralNode):
    def __init__(self, value, radix=10):
        self.value = value
        self.radix = radix

class IntNode(LiteralNode):
    def __init__(self, num_bits, is_signed, value, radix=10):
        self.num_bits = num_bits
        self._is_signed = is_signed
        self.value = str(value)
        self.radix = radix
        self.is_signed = is_signed

class NilNode(LiteralNode):
    pass

class SymbolNode(ExprNode):
    def __init__(self, id):
        self.id = id

class AttrNode(ExprNode):
    def __init__(self, id):
        self.id = id

class StringNode(LiteralNode):
    def __init__(self, value):
        self.value = value

class CGlobalVariable(ExprNode):
    def __init__(self, type_expr, id):
        self.type = type_expr
        self.id = id
