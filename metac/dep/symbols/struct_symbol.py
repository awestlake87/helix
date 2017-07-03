
from ..symbol import Symbol, mangle_qualified_name
from ..targets import StructTarget
from ..scope import Scope

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
                [ attr_type for attr_type, _ in self._attrs ]
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
