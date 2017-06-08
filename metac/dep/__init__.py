
from ..err import SymbolNotFound, SymbolAlreadyExists

import json

class Target:
    def __init__(self, deps=[ ]):
        self._deps = deps
        self._met = False

    def is_met(self):
        return self._met

    def add_dep(self, dep):
        self._deps.append(dep)

    def has_unmet_deps(self):
        for dep in self._deps:
            if not dep.is_met():
                return True

        return False

    def to_json(self):
        return [ dep.to_json() for dep in self._deps ]

    def __repr__(self):
        return json.dumps(self.to_json(), indent=4, sort_keys=True)


class UnitTarget(Target):
    pass

class FunTarget(Target):
    def __init__(self, id, fun_type, param_ids, body):
        super().__init__()
        self._id = id
        self._fun_type = fun_type
        self._param_ids = param_ids
        self._body = body

    def to_json(self):
        return {
            "name": self._id,
            "deps": [ dep.to_json() for dep in self._deps ]
        }

class StructTarget(Target):
    def __init__(self, id):
        super().__init__()

        self._id = id

    def to_json(self):
        return {
            "name": self._id,
            "deps": [ dep.to_json() for dep in self._deps ]
        }

class Symbol:
    def is_unit(self):
        return False

    def is_struct(self):
        return False

    def is_fun(self):
        return False

    def can_overload(self):
        return Falses

    def get_scope(self):
        return self.__repr__()

class UnitSymbol(Symbol):
    def __init__(self, block_node, parent_scope=None):
        self._scope = Scope(parent_scope)
        self._block_node = block_node

        self._block_node.hoist(self._scope)

    def get_scope(self):
        return self._scope

    def get_target(self):
        return UnitTarget(self._block_node.create_targets(self._scope))

    def is_unit(self):
        return True

class MetaFunSymbol(Symbol):
    def __init__(self, id, overloads=[ ]):
        self._id = id
        self._overloads = overloads

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
    def __init__(self, type, param_ids, body):
        self._id = id
        self._type = type
        self._param_ids = param_ids
        self._body = body

    def __repr__(self):
        return "meta overload"

class ExternFunSymbol(Symbol):
    def __init__(self, id, type, param_ids, body):
        self._id = id
        self._type = type
        self._param_ids = param_ids
        self._body = body

        self._target = FunTarget(
            self._id,
            self._type,
            self._param_ids,
            self._body
        )

    def get_target(self, scope):
        return self._target

    def __repr__(self):
        return "extern fun"

class InternFunSymbol(Symbol):
    def __init__(self, id, type, param_ids, body):
        self._id = id
        self._type = type
        self._param_ids = param_ids
        self._body = body

        self._target = FunTarget(
            self._id,
            self._type,
            self._param_ids,
            self._body
        )

    def get_target(self, scope):
        return self._target

    def __repr__(self):
        return "intern fun"

class StructSymbol(Symbol):
    def __init__(self, id):
        self._id = id

    def is_struct(self):
        return True

    def get_target(self, scope):
        return StructTarget(self._id)

    def __repr__(self):
        return "struct"

class Scope:
    def __init__(self, parent=None):
        self._parent = parent
        self._symbols = { }

    def to_dict(self):
        symbol_dict = { }

        for id, symbol in self._symbols.items():
            scope = symbol.get_scope()

            if type(scope) is Scope:
                symbol_dict[id] = scope.to_dict()
            else:
                symbol_dict[id] = scope

        return symbol_dict

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    def insert(self, id, target):
        if not self.has_local(id):
            self._symbols[id] = target
        else:
            raise SymbolAlreadyExists(id)

    def has_local(self, id):
        if id in self._symbols:
            return True
        else:
            return False


    def resolve(self, id):
        if self.has_local(id):
            return self._symbols[id]
        else:
            return self._parent.resolve(id)
