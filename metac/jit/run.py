from ctypes import CFUNCTYPE, c_int

import llvmlite.binding as binding

from ..err import Todo

from ..info import UnitProtoTarget, FunProtoTarget, FunTarget
from ..ir import *

def run(unit_target):
    class Context:
        def __init__(self):
            self.llvm_target = binding.Target.from_default_triple()
            self.llvm_target_machine = self.llvm_target.create_target_machine()
            self.llvm_backing_module = binding.parse_assembly("")

            self.llvm_engine = binding.create_mcjit_compiler(
                self.llvm_backing_module, self.llvm_target_machine
            )

    ctx = Context()

    while perform_build_pass(ctx, unit_target) != 0:
        # as long as we can keep building targets, it's working
        pass

    if unit_target.built:
        ctx.llvm_engine.finalize_object()

        jit_fun = CFUNCTYPE(c_int)(
            ctx.llvm_engine.get_function_address("__jit__")
        )

        return jit_fun()

    else:
        raise Todo("unable to build deps")

def perform_build_pass(ctx, target):
    if target.marked:
        return 0

    num_built = 0

    with target.mark():
        if not target.built:
            unbuilt_deps = False

            for dep in target.deps:
                if not dep.built:
                    unbuilt_deps = True
                    num_built += perform_build_pass(ctx, dep)

            if not unbuilt_deps and not target.built:
                build_target(ctx, target)
                num_built += 1
                target.built = True

        target.marked = False

    return num_built

def build_target(ctx, target):
    target_type = type(target)

    if target_type is UnitProtoTarget:
        target._ir_value = UnitValue("test")

    elif target_type is FunProtoTarget:
        target._ir_value = FunValue(
            target.unit_proto.ir_value,
            target.absolute_id,
            FunType(
                gen_static_expr_ir(target.scope, target.type.ret_type),
                [
                    gen_static_expr_ir(target.scope, param_type)
                    for param_type in
                    target.type.param_types
                ]
            )
        )

    elif target_type is FunTarget:
        gen_code(target.proto_target.ir_value, target.scope, target.info)

    elif target_type is UnitTarget:
        llvm_module = binding.parse_assembly(
            str(target.proto_target.ir_value.get_llvm_value())
        )

        llvm_module.verify()

        ctx.llvm_engine.add_module(llvm_module)

    else:
        raise Todo(target_type)
