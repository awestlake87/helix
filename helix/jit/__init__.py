
from ..dep import *

def build_target(target):
    target._build_target()

def perform_build_pass(target):
    if target.marked:
        return 0
    else:
        target.marked = True

    num_built = 0

    if not target.built:
        unbuilt_deps = False

        for dep in target.deps:
            if not dep.built:
                unbuilt_deps = True
                num_built += perform_build_pass(dep)

        if not unbuilt_deps and not target.built:
            build_target(target)
            num_built += 1
            target.built = True

    target.marked = False

    return num_built


def run(target):
    while perform_build_pass(target) != 0: pass

    if target.built:
        return target.run()
    else:
        raise Todo("unable to build")
