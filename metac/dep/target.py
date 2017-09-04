
import json

from ..err import Todo

class Target:
    def __init__(self, deps=[ ]):
        self.deps = deps

#        self._marked = False
#        self._built = False

#    def add_dep(self, dep):
#        self._deps.append(dep)

#    def build(self):
#        if not self.is_built():
#            while self._perform_build_pass() != 0: pass

#            if self.is_built():
#                return
#            else:
#                raise Todo("unable to build")


#    def _build_target(self):
#        raise Todo("implement build for {}".format(self))

#    def _perform_build_pass(self):
#        if self._marked:
#            return 0
#        else:
#            self._marked = True

#        num_built = 0

#        if not self.is_built():
#            unbuilt_deps = False

#            for dep in self._deps:
#                if not dep.is_built():
#                    unbuilt_deps = True
#                    num_built += dep._perform_build_pass()

#            if not unbuilt_deps and not self.is_built():
#                self._build_target()
#                num_built += 1
#                self._built = True

#        self._marked = False

#        return num_built

#    def is_built(self):
#        return self._built
