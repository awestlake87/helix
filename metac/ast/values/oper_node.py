from ..expr_node import ExprNode

from ..types import VoidTypeNode, FunTypeNode
from .fun_node import FunNode

class ConstructOperNode(FunNode):
    def __init__(self, param_types, param_ids, body):
        super().__init__(
            FunTypeNode(VoidTypeNode(), param_types),
            "construct",
            param_ids,
            body,
            is_attr=True
        )

class DestructOperNode(FunNode):
    def __init__(self, body):
        super().__init__(
            FunTypeNode(VoidTypeNode(), [ ]),
            "destruct",
            [ ],
            body,
            is_attr=True
        )
