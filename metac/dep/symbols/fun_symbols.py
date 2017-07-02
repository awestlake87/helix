
from ..symbol import Symbol
from ..targets import FunTarget

from ...err import Todo

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

    def get_scope(self):
        overloads = [ ]

        for overload in self._overloads:
            overloads.append(overload.get_scope())

        return overloads

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

    def matches(self, scope, args):
        if len(self._type._param_types) == len(args):
            return True
        else:
            return False

    def get_call_deps(self, scope, args):
        return [
            FunTarget(
                self._parent_scope,
                self._id,
                self._type,
                self._param_ids,
                self._body
            )
        ]

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

    def get_call_deps(self, scope, args):
        return [ self.get_target() ]

    def get_target(self):
        if self._target is None:
            self._target = FunTarget(
                self._parent_scope,
                self._id,
                self._type,
                self._param_ids,
                self._body
            )

        return self._target

    def __repr__(self):
        return "extern fun"

class InternFunSymbol(Symbol):
    def __init__(self, parent_scope, id, type, param_ids, body):
        self._parent_scope = parent_scope
        self._id = id
        self._type = type
        self._param_ids = param_ids
        self._body = body

        self._target = None

    def get_call_deps(self, scope, args):
        return [ self.get_target() ]

    def get_target(self):
        if self._target is None:
            self._target = FunTarget(
                self._parent_scope,
                self._id,
                self._type,
                self._param_ids,
                self._body
            )

        return self._target

    def __repr__(self):
        return "intern fun"
