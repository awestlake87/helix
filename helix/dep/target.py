
import json

from ..err import Todo

class Target:
    def __init__(self, deps):
        self.deps = deps

        self.marked = False
        self.built = False

    def build(self):
        raise Todo("implement build for {}".format(self))
