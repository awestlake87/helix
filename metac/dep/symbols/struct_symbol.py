
from ..symbol import Symbol, mangle_qualified_name
from ..scope import Scope
from ..target import Target

class StructTarget(Target):
    def __init__(self, id, parent_scope, attrs):
        self._id = id
        self._parent_scope = parent_scope
        self._attrs = attrs

        deps = [ ]

        for attr_type, _ in self._attrs:
            target = attr_type.get_value(self._parent_scope).get_target()
            if target:
                deps.append(target)

        super().__init__(deps)

    def _get_target_name(self):
        return "struct {}".format(
            self._parent_scope.get_qualified_name(self._id)
        )

    def _build_target(self):

        print("create ir value for {}".format(self._get_target_name()))

    def to_json(self):
        return {
            "name": self._parent_scope.get_qualified_name(self._id),
            "deps": [ dep.to_json() for dep in self._deps ]
        }

class StructSymbol(Symbol):
    def __init__(self, id, attrs, parent_scope):
        self._id = id
        self._parent_scope = parent_scope
        self._scope = Scope(self._parent_scope)
        self._attrs = attrs

        for attr_type, _ in attrs:
            attr_type.hoist(self._scope)

        self._target = None

    def get_target(self):
        if self._target is None:
            self._target = StructTarget(
                self._id,
                self._parent_scope,
                self._attrs
            )

        return self._target


    def get_mangled_name(self):
        return mangle_qualified_name(
            self._parent_scope.get_qualified_name(self._id)
        )

    def get_call_deps(self, scope, args):
        return [ self.get_target() ]

    def is_struct(self):
        return True

    def __repr__(self):
        return "struct"
