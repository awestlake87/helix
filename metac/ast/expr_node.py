
from .statements import StatementNode

class ExprNode(StatementNode):

    def hoist(self, scope):
        pass

    def get_deps(self, scope):
        return [ ]

    def gen_module_code(self, module):
        self.gen_module_value(module)

    def gen_unit_code(self, unit):
        self.gen_unit_value(unit)

    def gen_fun_code(self, block):
        self.gen_fun_value(block)

class UnaryExprNode(ExprNode):
    def __init__(self, operand):
        self._operand = operand

    def hoist(self, scope):
        self._operand.hoist(scope)

    def get_deps(self, scope):
        return self._operand.get_deps(scope)

class BinaryExprNode(ExprNode):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    def hoist(self, scope):
        self._lhs.hoist(scope)
        self._rhs.hoist(scope)

    def get_deps(self, scope):
        return (
            self._lhs.get_deps(scope) + self._rhs.get_deps(scope)
        )
