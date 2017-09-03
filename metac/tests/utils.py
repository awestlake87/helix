from ..ast import parse_unit
from ..sym import UnitSymbol
from ..dep import JitTarget

def run_test(code, emit_ir=False):
    unit = UnitSymbol("test", parse_unit(code))
    
    jit_target = JitTarget([ unit ])

    jit_target.build()

    if emit_ir:
        print(unit.get_llvm_module())

    return jit_target.run()
