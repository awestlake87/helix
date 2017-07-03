
from ..target import Target

class StructTarget(Target):
    def __init__(self, id, parent_scope, attr_types):
        self._id = id
        self._parent_scope = parent_scope

        deps = [ ]

        for attr in attr_types:
            target = attr.get_value(self._parent_scope).get_target()
            if target:
                deps.append(target)

        super().__init__(deps)

    def _build_target(self):
        print(
            "build struct {}".format(
                self._parent_scope.get_qualified_name(self._id)
            )
        )

    def to_json(self):
        return {
            "name": self._parent_scope.get_qualified_name(self._id),
            "deps": [ dep.to_json() for dep in self._deps ]
        }
