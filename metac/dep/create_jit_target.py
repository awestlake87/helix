
from .target import Target

from .get_deps import get_block_deps

class JitTarget(Target):
    def __init__(self, deps):
        super().__init__(deps)

    def _build_target(self):
        print("build jit")

def create_jit_target(scope, ast):
    return JitTarget(get_block_deps(scope, ast))
