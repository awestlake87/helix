from ...target import Target
from ...scope import Scope

import llvmlite

class FunTarget(Target):
    def __init__(
        self,
        symbol,
        parent_scope,
        id,
        fun_type,
        param_ids,
        body,
        on_proto_built
    ):
        self._symbol = symbol
        self._parent_scope = parent_scope
        self._scope = Scope(id, parent_scope)
        self._id = id
        self._fun_type = fun_type
        self._param_ids = param_ids
        self._body = body
        self._on_proto_built_callback = on_proto_built
        self._ir_fun = None

        self._body.hoist(self._scope)

        self._proto_target = FunProtoTarget(
            parent_scope, id, fun_type, param_ids, self, self._on_proto_built
        )

        super().__init__(
            self._proto_target.get_deps() +
            self._body.get_deps(self._scope)
        )

    def _on_proto_built(self, ir_fun):
        self._ir_fun = ir_fun
        self._on_proto_built_callback(ir_fun)

    def get_proto_target(self):
        return self._proto_target

    def _get_target_name(self):
        return "fun {}({})".format(
            self._parent_scope.get_qualified_name(self._id),
            ", ".join(self._param_ids)
        )

    def _build_target(self):
        self._proto_target.build()

        print("write ir for {}".format(str(self._ir_fun).strip()))

        self._body.gen_code(self._symbol, self._scope)

        print(self._ir_fun.module)

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
