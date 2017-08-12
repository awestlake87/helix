
from ...symbol import Symbol, mangle_qualified_name

from ....err import Todo

from .targets import FunTarget, FunProtoTarget

class MetaFunSymbol(Symbol):
    def __init__(self, id, overloads=[ ]):
        self._id = id
        self._overloads = overloads

    def get_call_deps(self, scope, args):
        selected = None

        for overload in self._overloads:
            if overload.matches(scope, args):
                if selected is None:
                    selected = overload
                else:
                    raise Todo("call to {}(...) is ambiguous".format(self._id))

        if selected:
            return selected.get_call_deps(scope, args)

        else:
            raise Todo(
                "call to {}(...) does not match any known overloads".format(
                    self._id
                )
            )

    def is_fun(self):
        return True

    def can_overload(self):
        return True

    def add_overload(self, symbol):
        self._overloads.append(symbol)

class MetaOverloadSymbol(Symbol):
    def __init__(self, parent_scope, id, type, param_ids, body):
        self._parent_scope = parent_scope
        self._id = id
        self._type = type
        self._param_ids = param_ids
        self._body = body

        self._targets = { }

    def matches(self, scope, args):
        if len(self._type._param_types) == len(args):
            return True
        else:
            return False

    def _on_proto_built(self, ir_fun):
        self._ir_fun = ir_fun

    def get_target(self, scope, args):
        name = "_ZN{}{}".format(
            mangle_qualified_name(
                self._parent_scope.get_qualified_name(self._id)
            ),
            "_".join([
                "arg" for arg in args
            ])
        )

        if not name in self._targets:
            target = FunTarget(
                self,
                self._parent_scope,
                self._id,
                self._type,
                self._param_ids,
                self._body,
                on_proto_built=self._on_proto_built
            )
            self._targets[name] = target
            return target

        else:
            return self._targets[name]

    def get_proto_target(self, scope, args):
        return self.get_target(scope, args).get_proto_target()

    def get_call_deps(self, scope, args):
        return [ self.get_proto_target(scope, args) ]

    def __repr__(self):
        return "({})".format(", ".join(self._param_ids))

class ExternFunSymbol(Symbol):
    def __init__(self, parent_scope, id, type, param_ids, body):
        self._parent_scope = parent_scope
        self._id = id
        self._type = type
        self._param_ids = param_ids
        self._body = body

        self._target = None
        self._ir_fun = None

    def _on_proto_built(self, ir_fun):
        self._ir_fun = ir_fun

    def get_call_deps(self, scope, args):
        return [ self.get_proto_target() ]

    def get_target(self):
        if self._target is None:
            self._target = FunTarget(
                self,
                self._parent_scope,
                self._id,
                self._type,
                self._param_ids,
                self._body,
                on_proto_built=self._on_proto_built
            )

        return self._target

    def get_proto_target(self):
        return self.get_target().get_proto_target()

    def __repr__(self):
        return "extern fun"
