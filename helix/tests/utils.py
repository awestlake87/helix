from ..ast import parse_unit
from ..sym import gen_unit_sym, JitTarget, hoist_block
from ..dep import gen_unit_deps
from ..jit import run

def run_test(code, emit_ir=False):
    unit_node = parse_unit("test", code)
    unit_sym = gen_unit_sym(unit_node)

    hoist_block(unit_sym, unit_sym.ast.block)

    unit_sym.target.deps += gen_unit_deps(unit_sym)

    jit_target = JitTarget([ unit_sym ])

    result = run(jit_target)

    if emit_ir:
        print(unit_sym.get_llvm_module())

    return result
