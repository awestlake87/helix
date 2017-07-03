
from ..target import Target
from ..scope import Scope

class FunTarget(Target):
    def __init__(self, parent_scope, id, fun_type, param_ids, body):
        self._parent_scope = parent_scope
        self._scope = Scope(id, parent_scope)
        self._id = id
        self._fun_type = fun_type
        self._param_ids = param_ids
        self._body = body

        self._body.hoist(self._scope)
        super().__init__(
            self._fun_type.get_deps(parent_scope) +
            self._body.get_deps(self._scope)
        )

        self._proto_target = FunProtoTarget(
            parent_scope, id, fun_type, param_ids, self
        )

    def get_proto_target(self):
        return self._proto_target

    def _build_target(self):
        print(
            "build fun {}({})".format(
                self._parent_scope.get_qualified_name(self._id),
                ", ".join(self._param_ids)
            )
        )

    def to_json(self):
        return {
            "name": "{}({})".format(
                self._parent_scope.get_qualified_name(self._id),
                ", ".join(self._param_ids)
            ),
            "deps": [ dep.to_json() for dep in self._deps ],
            "scope": self._scope.to_dict()
        }

class FunProtoTarget(Target):
    def __init__(self, parent_scope, id, fun_type, param_ids, fun_target):
        self._parent_scope = parent_scope
        self._id = id
        self._fun_type = fun_type
        self._param_ids = param_ids
        self._fun_target = fun_target

        super().__init__(
            self._fun_type.get_deps(self._parent_scope),
            [ self._fun_target ]
        )

    def _build_target(self):
        print(
            "build fun proto {}({})".format(
                self._parent_scope.get_qualified_name(self._id),
                ", ".join(self._param_ids)
            )
        )

    def to_json(self):
        return {
            "name": "{}({}) proto".format(
                self._parent_scope.get_qualified_name(self._id),
                ", ".join(self._param_ids)
            ),
            "deps": [ dep.to_json() for dep in self._deps ],
            "post_deps": [ dep.to_json() for dep in self._post_deps ]
        }
