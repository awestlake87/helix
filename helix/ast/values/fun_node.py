
from ..expr_node import ExprNode

from ...err import Todo

class FunNode(ExprNode):
    def __init__(
        self,
        type,
        id,
        param_ids,
        body,
        is_vargs = False,
        is_attr = False,
        is_cfun = False,
        is_mut = False
    ):
        self.type = type
        self.id = id
        self.param_ids = param_ids
        self.body = body
        self.is_cfun = is_cfun

        self.is_vargs = is_vargs
        self.is_attr = is_attr
        self.is_mut = is_mut

        if self.is_cfun:
            if self.is_attr:
                raise Todo("cfuns cannot be attr funs")

        else:
            if self.is_vargs:
                raise Todo("vargs is only applicable to cfuns")

        if not self.is_attr:
            if self.is_mut:
                raise Todo("mut is only applicable to attr funs")
