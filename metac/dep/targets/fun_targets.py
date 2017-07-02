
from ..target import Target
from ..scope import Scope

class FunTarget(Target):
    def __init__(self, parent_scope, id, fun_type, param_ids, body):

        self._scope = Scope(parent_scope)
        self._id = id
        self._fun_type = fun_type
        self._param_ids = param_ids
        self._body = body

        self._body.hoist(self._scope)
        super().__init__(
            self._fun_type.get_deps(parent_scope) +
            self._body.get_deps(self._scope)
        )

    def _build_target(self):
        print("build {}".format(self._id))

    def to_json(self):
        return {
            "name": "{}({})".format(self._id, ", ".join(self._param_ids)),
            "deps": [ dep.to_json() for dep in self._deps ],
            "scope": self._scope.to_dict()
        }
