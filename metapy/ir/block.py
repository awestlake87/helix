
from ..err import ReturnTypeMismatch, Todo
from .symbols import SymbolTable

class Block:
    def __init__(self, fun, parent, name):
        self._fun = fun
        self._parent = parent
        self._builder = fun._builder

        self._first = self._builder.append_basic_block(name)
        self._current = self._first

        self.symbols = SymbolTable(
            parent.symbols if parent != None else fun._unit.symbols
        )

    def get_unit(self):
        return self._fun._unit

    def create_return(self, value):
        self._builder.position_at_end(self._current)

        if value.type.can_convert_to(self._fun.type._ret_type):
            ret_value = value.as_type(self._fun.type._ret_type, self._builder)
            self._builder.ret(ret_value.get_llvm_rval(self._builder))

        else:
            raise ReturnTypeMismatch()
