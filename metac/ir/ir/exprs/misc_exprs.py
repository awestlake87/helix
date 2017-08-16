from ...err import Todo, CompilerBug
from ..values.values import *
from ..values.fun import Fun
from ..types import *

from llvmlite import ir

def gen_fun_as(fun, value, as_type):
    if not value.type.can_convert_to(as_type):
        raise NoImplicitCast()

    type_of = type(value)

    if type_of == NilValue:
        return NilValue(as_type)

    elif type_of == StaticValue:
        return StaticValue(as_type, value._value)

    else:
        return value

def gen_fun_assign(fun, lhs, rhs):
    if not rhs.type.can_convert_to(lhs.type):
        raise CompilerBug("type mismatch in function level assign")

    if type(lhs) is FunLlvmLVal:
        fun._builder.store(
            gen_fun_as(fun, rhs, lhs.type).get_llvm_rval(),
            lhs._value
        )
        return lhs

    else:
        raise Todo()

def gen_fun_dot(fun, lhs, rhs):
    if type(lhs.type) is StructType:
        if type(rhs) is str:
            attr_type, attr_index = lhs.type.get_attr_info(rhs)

            return FunLlvmLVal(
                fun,
                attr_type,
                fun._builder.gep(
                    lhs.get_llvm_lval(),
                    [ ir.IntType(32)(0), ir.IntType(32)(attr_index) ]
                )
            )

        else:
            raise Todo("make a \"rhs of '.' must be an identifier\" error")

    else:
        raise Todo()



def gen_fun_call(fun, lhs, args):
    if type(lhs) is Fun:
        if len(args) != len(lhs.type._param_types):
            raise Todo("arg length mismatch")

        llvm_args = [ ]

        for ty, arg in zip(lhs.type._param_types, args):
            if arg.type.can_convert_to(ty):
                arg_value = gen_fun_as(fun, arg, ty)
                llvm_args.append(arg_value.get_llvm_rval())

            else:
                raise NotApplicable()

        return ConstLlvmValue(
            lhs.type._ret_type, fun._builder.call(lhs._fun, llvm_args)
        )

    elif type(lhs) is IntType:
        if len(args) != 1:
            raise Todo("invalid args")

        if args[0].type.can_convert_to(lhs):
            return gen_fun_as(fun, args[0], lhs)
        else:
            raise Todo("invalid args")

    elif type(lhs) is StructType:
        if len(args) != 0:
            raise Todo("struct ctor args")

        return FunLlvmRVal(
            fun,
            lhs,
            lhs.get_llvm_type()(ir.Undefined)
        )

    else:
        raise Todo()
