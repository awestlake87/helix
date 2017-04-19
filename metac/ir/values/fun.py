
from ...err import ReturnTypeMismatch, NotApplicable, Todo
from ..symbols import SymbolTable
from .values import Value, LlvmRhsValue

from llvmlite import ir

class Fun(Value):
    EXTERN_C = 0
    INTERN_C = 1


    def __init__(self, unit, type, id, param_ids, linkage):
        self.unit = unit
        self.type = type

        self._builder = None
        self._id = id
        self._fun = ir.Function(
            unit._module, self.type.get_llvm_type(self._builder), id
        )

        for arg, id in zip(self._fun.args, param_ids):
            arg.name = id

        if linkage == Fun.EXTERN_C:
            self._fun.linkage = "external"

        elif linkage == Fun.INTERN_C:
            self._fun.linkage = "internal"

    def create_body(self):
        self._entry = self._fun.append_basic_block("entry")

        self._builder = ir.IRBuilder(self._entry)

        self._body = self._builder.append_basic_block("body")
        self._builder.branch(self._body)
        self._builder.position_at_end(self._body)

        self.symbols = SymbolTable(self.unit.symbols)

        for type, arg in zip(self.type._param_types, self._fun.args):
            self.symbols.insert(arg.name, LlvmRhsValue(type, arg))

    def call(self, fun, args):
        if len(args) != len(self.type._param_types):
            raise Todo("arg length mismatch")

        llvm_args = [ ]

        for type, arg in zip(self.type._param_types, args):
            if arg.type.can_convert_to(type):
                arg_value = arg.as_type(type, fun._builder)
                llvm_args.append(arg_value.get_llvm_rval(fun._builder))

            else:
                raise NotApplicable()

        return LlvmRhsValue(
            self.type._ret_type, fun._builder.call(self._fun, llvm_args)
        )

    def create_return(self, value):
        if value.type.can_convert_to(self.type._ret_type):
            ret_value = value.as_type(self.type._ret_type, self._builder)
            self._builder.ret(ret_value.get_llvm_rval(self._builder))

        else:
            raise ReturnTypeMismatch()

    def is_rval(self):
        return True

    def get_llvm_rval(self, builder):
        return self._fun
