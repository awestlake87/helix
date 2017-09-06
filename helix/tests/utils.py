from ..ast import parse_unit
from ..sym import UnitSymbol, JitTarget
from ..dep import gen_unit_deps
from ..jit import run

def run_test(code, emit_ir=False):
    unit = UnitSymbol("test", parse_unit(code))

    unit.target.deps += gen_unit_deps(unit)

    jit_target = JitTarget([ unit ])

    result = run(jit_target)

    if emit_ir:
        print(unit.get_llvm_module())

    return result
