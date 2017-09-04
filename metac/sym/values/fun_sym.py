
from ...scope import Scope

from ..expr_sym import ExprSym

class FunSym(ExprSym):
    def __init__(
        self,
        parent_scope,
        id,
        fun_type_sym,
        param_ids,
        is_cfun = False
    ):
        self.parent_scope = parent_scope
        self.scope = Scope(self.parent_scope)
        self.id = id
        self.type = fun_type_sym
        self.param_ids = param_ids
        self.is_cfun = is_cfun

        self.body = None
