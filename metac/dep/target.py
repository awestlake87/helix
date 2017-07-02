
import json

from ..err import Todo

class Target:
    def __init__(self, deps=[ ]):
        self._deps = deps
        self._met = False

    def build(self):
        if not self.is_met():
            while self._perform_build_pass() != 0: pass

            if self.is_met():
                return
            else:
                raise Todo("unable to build")

    def _build_target(self):
        raise Todo("implement build for {}".format(self))

    def _perform_build_pass(self):
        unmet_deps = False
        num_built = 0

        for dep in self._deps:
            if not dep.is_met():
                unmet_deps = True
                num_built += dep._perform_build_pass()

        if not unmet_deps and not self.is_met():
            self._build_target()
            num_built += 1
            self._met = True

        return num_built

    def is_met(self):
        return self._met

    def add_dep(self, dep):
        self._deps.append(dep)

    def has_unmet_deps(self):
        for dep in self._deps:
            if not dep.is_met():
                return True

        return False

    def to_json(self):
        return [ dep.to_json() for dep in self._deps ]

    def __repr__(self):
        return json.dumps(self.to_json(), indent=4, sort_keys=True)
