
from ..symbol import Symbol, mangle_qualified_name
from ..scope import Scope
from ..target import Target
from ...err import CircularDependency, CircularAttrDependency

from llvmlite import ir

class StructTarget(Target):
    def __init__(self, id, parent_scope, attrs, on_built):
        self._id = id
        self._parent_scope = parent_scope
        self._attrs = [
            (type.get_value(self._parent_scope), id) for type, id in attrs
        ]
        self._on_built = on_built

        deps = [ ]

        for attr_type, attr_id in self._attrs:
            try:
                target = attr_type.get_target()

                if target:
                    deps.append(target)

            except CircularDependency as e:
                raise CircularAttrDependency(self._id, attr_id)

        super().__init__(deps)

    def _build_target(self):
        self._on_built(
            ir.LiteralStructType(
                [ type.get_ir_type() for type, _ in self._attrs ]
            )
        )

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
        self._creating_target = False

    def _on_built(self, ir_type):
        self._ir_type = ir_type
        print(self._ir_type)

    def get_target(self):
        if self._target is None:
            if not self._creating_target:
                self._creating_target = True
                self._target = StructTarget(
                    self._id,
                    self._parent_scope,
                    self._attrs,
                    on_built=self._on_built
                )
                self._creating_target = False
            else:
                raise CircularDependency()

        return self._target

    def get_ir_type(self):
        return self._ir_type

    def get_mangled_name(self):
        return mangle_qualified_name(
            self._parent_scope.get_qualified_name(self._id)
        )

    def get_call_deps(self, scope, args):
        return [ self.get_target() ]

    def is_struct(self):
        return True
