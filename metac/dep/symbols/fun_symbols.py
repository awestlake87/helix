
from ..symbol import Symbol, mangle_qualified_name

from ...err import Todo

from ..target import Target
from ..scope import Scope

import llvmlite

class FunTarget(Target):
    def __init__(
        self,
        parent_scope,
        id,
        fun_type,
        param_ids,
        body,
        on_proto_built
    ):
        self._parent_scope = parent_scope
        self._scope = Scope(id, parent_scope)
        self._id = id
        self._fun_type = fun_type
        self._param_ids = param_ids
        self._body = body

        self._body.hoist(self._scope)

        self._proto_target = FunProtoTarget(
            parent_scope, id, fun_type, param_ids, self, on_proto_built
        )

        super().__init__(
            self._proto_target.get_deps() +
            self._body.get_deps(self._scope)
        )

    def get_proto_target(self):
        return self._proto_target

    def _get_target_name(self):
        return "fun {}({})".format(
            self._parent_scope.get_qualified_name(self._id),
            ", ".join(self._param_ids)
        )

    def _build_target(self):
        self._proto_target.build()
        print("write ir for {}".format(self._get_target_name()))

        for target in self._deps:
            if type(target) is FunTarget:
                print(
                    "link {} into {}".format(
                        target._get_target_name(),
                        self._get_target_name()
                    )
                )

    def _meet_target(self):
        for target in self._deps:
            if type(target) is FunProtoTarget:
                print(
                    "link {} into {}".format(
                        target._get_target_name(),
                        self._get_target_name()
                    )
                )


    def to_json(self):
        return {
            "name": self._get_target_name(),
            "deps": [ dep.to_json() for dep in self._deps ],
            "scope": self._scope.to_dict()
        }

class FunProtoTarget(Target):
    def __init__(
        self,
        parent_scope,
        id,
        fun_type,
        param_ids,
        fun_target,
        on_proto_built
    ):
        self._parent_scope = parent_scope
        self._id = id
        self._ret_type = fun_type._ret_type.get_value(self._parent_scope)
        self._params = [
            (type.get_value(self._parent_scope), id)
            for type, id in
            zip(fun_type._param_types, param_ids)
        ]

        self._fun_target = fun_target
        self._on_proto_built = on_proto_built

        super().__init__(
            fun_type.get_deps(self._parent_scope),
            [ self._fun_target ]
        )

    def _get_param_ids(self):
        return [ id for _, id in self._params ]

    def _get_target_name(self):
        return "fun proto {}({})".format(
            self._parent_scope.get_qualified_name(self._id),
            ", ".join(self._get_param_ids())
        )

    def _build_target(self):
        module = llvmlite.ir.Module(self._get_target_name())
        fun_type = llvmlite.ir.FunctionType(
            self._ret_type.get_ir_type(),
            [ type.get_ir_type() for type, _ in self._params ]
        )

        ir_fun = llvmlite.ir.Function(module, fun_type, self._id)
        ir_fun.linkage = "external"

        for arg, (_, id) in zip(ir_fun.args, self._params):
            arg.name = id

        self._on_proto_built(ir_fun)

    def to_json(self):
        return {
            "name": self._get_target_name(),
            "deps": [ dep.to_json() for dep in self._deps ],
            "post_deps": [ dep.to_json() for dep in self._post_deps ]
        }


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
        print(ir_fun)
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
        print(ir_fun)
        self._ir_fun = ir_fun

    def get_call_deps(self, scope, args):
        return [ self.get_proto_target() ]

    def get_target(self):
        if self._target is None:
            self._target = FunTarget(
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

class InternFunSymbol(Symbol):
    def __init__(self, parent_scope, id, type, param_ids, body):
        self._parent_scope = parent_scope
        self._id = id
        self._type = type
        self._param_ids = param_ids
        self._body = body

        self._target = None
        self._ir_fun = None

    def _on_proto_built(self, ir_fun):
        print(ir_fun)
        self._ir_fun = ir_fun

    def get_call_deps(self, scope, args):
        return [ self.get_proto_target() ]

    def get_target(self):
        if self._target is None:
            self._target = FunTarget(
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
        return "intern fun"
