
from .statements import StatementNode

class ExprNode(StatementNode):
    def gen_module_code(self, module):
        self.gen_module_value(module)

    def gen_unit_code(self, unit):
        self.gen_unit_value(unit)

    def gen_fun_code(self, block):
        self.gen_fun_value(block)

class UnaryExprNode(ExprNode):
    def __init__(self, operand):
        self._operand = operand

class BinaryExprNode(ExprNode):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs
