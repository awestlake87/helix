from ..ast import parse_unit
from ..sym import UnitSymbol
from ..dep import JitTarget
from ..jit import run

def run_test(code, emit_ir=False):
    unit = UnitSymbol("test", parse_unit(code))

    jit_target = JitTarget([ unit ])

    result = run(jit_target)

    if emit_ir:
        print(unit.get_llvm_module())

    return result
