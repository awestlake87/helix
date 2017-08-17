from ..lang import Parser
from ..sym import UnitSymbol
from ..dep import JitTarget

def run_test(code):
    parser = Parser(code)

    jit_target = JitTarget([ UnitSymbol("test", parser.parse()) ])

    jit_target.build()

    return jit_target.run()
