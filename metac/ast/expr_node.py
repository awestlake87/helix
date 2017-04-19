
from .statements import StatementNode

class ExprNode(StatementNode):
    def gen_module_code(self, module):
        self.gen_module_value(module)

    def gen_unit_code(self, unit):
        self.gen_unit_value(unit)

    def gen_fun_code(self, block):
        self.gen_fun_value(block)
