
import json

from ..err import Todo

class Target:
    def __init__(self, deps=[ ], post_deps=[ ]):
        # pre-requisites
        self._deps = deps
        # post-requisites
        self._post_deps = post_deps

        self._built = False
        self._met = False

        self._marked = False

    def get_deps(self):
        return self._deps

    def get_post_deps(self):
        return self._post_deps

    def build(self):
        if not self.is_built():
            while self._perform_build_pass() != 0: pass

            if self.is_built():
                return
            else:
                raise Todo("unable to build")

    def meet(self):
        if not self.is_met():
            while self._perform_build_pass() != 0: pass

            if self.is_met():
                return
            else:
                raise Todo("unable to meet")


    def _build_target(self):
        raise Todo("implement build for {}".format(self))

    def _meet_target(self):
        pass

    def _perform_build_pass(self):
        if self._marked:
            return 0
        else:
            self._marked = True

        num_built = 0

        if not self.is_built():
            unbuilt_deps = False

            for dep in self._deps:
                if not dep.is_built():
                    unbuilt_deps = True
                    num_built += dep._perform_build_pass()

            if not unbuilt_deps and not self.is_built():
                self._build_target()
                num_built += 1
                self._built = True

        elif not self.is_met():
            unmet_deps = False

            for dep in self._deps:
                if not dep.is_met():
                    unmet_deps = True
                    num_built += dep._perform_build_pass()

            for dep in self._post_deps:
                if not dep.is_met():
                    unmet_deps = True
                    num_built += dep._perform_build_pass()

            if not unmet_deps and not self.is_met():
                self._meet_target()
                self._met = True
                num_built += 1

        self._marked = False

        return num_built

    def is_built(self):
        return self._built

    def is_met(self):
        return self._met

    def to_json(self):
        return [ dep.to_json() for dep in self._deps ]

    def __repr__(self):
        return json.dumps(self.to_json(), indent=4, sort_keys=True)
