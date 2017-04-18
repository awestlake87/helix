
from ..ir import Unit, Fun, NilValue, AutoIntType, IntType, StaticValue
from ..err import Todo

from .exprs import ExprNode

class UnitNode(ExprNode):
    def __init__(self, block):
        self._block = block

    def gen_module_value(self, module):
        unit = Unit()

        self._block.hoist_unit_code(unit)
        self._block.gen_unit_code(unit)

        return unit

class FunNode(ExprNode):
    EXTERN_C = 0
    INTERN_C = 1

    def __init__(self, type, id, param_ids, linkage, body):
        self._type = type
        self._id = id
        self._param_ids = param_ids
        self._linkage = linkage
        self._body = body

    def _create_ir_fun(self, unit):
        linkage = None

        if self._linkage == FunNode.EXTERN_C:
            linkage = Fun.EXTERN_C
        elif self._linkage == FunNode.INTERN_C:
            linkage = Fun.INTERN_C
        else:
            raise Todo("handle error")

        return Fun(
            unit,
            self._type.gen_unit_value(unit),
            self._id,
            self._param_ids,
            linkage
        )

    def hoist_unit_code(self, unit):
        self._fun = self._create_ir_fun(unit)

        unit.symbols.insert(self._id, self._fun)

    def gen_unit_value(self, unit):
        self._fun.create_body()

        self._body.hoist_fun_code(self._fun)
        self._body.gen_fun_code(self._fun)

        return self._fun


    def hoist_fun_code(self, block):
        self._fun = self._create_ir_fun(block.get_unit())

        block.symbols.insert(self._id, self._fun)

    def gen_fun_value(self, block):
        return self.gen_unit_value(block.get_unit())


class AutoIntNode(ExprNode):
    def __init__(self, value, radix=10):
        self._value = value
        self._radix = radix

    def gen_unit_value(self, unit):
        return StaticValue(
            AutoIntType(),
            (
                int(self._value, self._radix)
                if type(self._value) is str else
                self._value
            )
        )

    def gen_fun_value(self, block):
        return self.gen_unit_value(block.get_unit())

class IntNode(ExprNode):
    def __init__(self, num_bits, is_signed, value, radix=10):
        self._num_bits = num_bits
        self._is_signed = is_signed
        self._value = value
        self._radix = radix

    def gen_unit_value(self, unit):
        return StaticValue(
            IntType(self._num_bits, self._is_signed),
            int(self._value, self._radix)
        )

class NilNode(ExprNode):
    def gen_unit_value(self, unit):
        return NilValue()

    def gen_fun_value(self, block):
        return self.gen_unit_value(block.get_unit())

class SymbolNode(ExprNode):
    def __init__(self, id):
        self._id = id

    def gen_unit_value(self, unit):
        return unit.symbols.resolve(self._id)

    def gen_fun_value(self, block):
        return block.symbols.resolve(self._id)
