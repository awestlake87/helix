from ..ast import parse_unit
from ..sym import gen_unit_sym
from ..info import gen_unit_info
from ..dep import gen_unit_target
from ..jit import run

def run_test(code, emit_ir=False):
    unit_node = parse_unit(code)
    unit_sym = gen_unit_sym(unit_node)
    unit_info = gen_unit_info(unit_sym)
    unit_target = gen_unit_target(unit_info)

    return run(unit_target)

    #unit = UnitSymbol("test", unit_node)

    #jit_target = JitTarget([ unit ])

    #jit_target.build()

    #if emit_ir:
    #    print(unit.get_llvm_module())

    #return jit_target.run()
