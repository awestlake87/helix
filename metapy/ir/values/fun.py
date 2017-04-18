
from ...err import ReturnTypeMismatch, NotApplicable, Todo
from ..block import Block
from .values import Value, LlvmRhsValue

from llvmlite import ir

class Fun(Value):
    EXTERN_C = 0
    INTERN_C = 1

    def __init__(self, unit, type, id, param_ids, linkage):
        self._unit = unit
        self._builder = None
        self.type = type
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
        self._body = Block(self, None, "body")

        for type, arg in zip(self.type._param_types, self._fun.args):
            self._body.symbols.insert(arg.name, LlvmRhsValue(type, arg))

        self._builder.branch(self._body._first)

        return self._body

    def call(self, block, args):
        self._builder.position_at_end(block._current)

        if len(args) != len(self.type._param_types):
            raise Todo("arg length mismatch")

        llvm_args = [ ]

        for type, arg in zip(self.type._param_types, args):
            if arg.type.can_convert_to(type):
                arg_value = arg.as_type(type, self._builder)
                llvm_args.append(arg_value.get_llvm_rval(self._builder))

            else:
                raise NotApplicable()

        return LlvmRhsValue(
            self.type._ret_type, self._builder.call(self._fun, llvm_args)
        )

    def is_rval(self):
        return True

    def get_llvm_rval(self, builder):
        return self._fun
