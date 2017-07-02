
from ..target import Target

class StructTarget(Target):
    def __init__(self, id):
        super().__init__()

        self._id = id

    def _build_target(self):
        print("build {}".format(self._id))

    def to_json(self):
        return {
            "name": self._id,
            "deps": [ dep.to_json() for dep in self._deps ]
        }
