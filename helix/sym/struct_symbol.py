
from .scope import Scope

from ..err import Todo
from ..dep import StructTarget

from ..ast import (
    DataAttr, FunNode, StructNode, ConstructOperNode, DestructOperNode
)

from .fun_symbol import FunSymbol, AttrFunSymbol
from .oper_symbol import ConstructOperSymbol, DestructOperSymbol

class DataAttrSymbol:
    def __init__(self, ast, index):
        self.ast = ast
        self.id = ast.id
        self.index = index

        self._ir_type = None
        self.type = None

    def set_ir_type(self, t):
        self._ir_type = t

    def get_ir_type(self):
        if self._ir_type is None:
            raise Todo()

        else:
            return self._ir_type

class StructSymbol:
    def __init__(self, unit, parent_scope, ast):
        self.unit = unit
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)
        self.ast = ast
        self.attrs = [ ]

        self.id = self.ast.id

        self.target = StructTarget(self, on_ir=self._on_ir)
        self._ir_value = None

        ids = { }

        attr_index = 0

        for attr_id, attr_node in self.ast.attrs:
            if attr_id not in ids:
                ids[attr_id] = attr_node
            else:
                raise Todo("duplicate name in struct")

            attr_type = type(attr_node)

            if attr_type is FunNode:
                if attr_node.is_attr:
                    self.attrs.append((
                        attr_id,
                        AttrFunSymbol(unit, self, attr_node, self.scope)
                    ))

                else:
                    self.attrs.append(
                        (attr_id, FunSymbol(unit, attr_node, self.scope))
                    )

            elif attr_type is StructNode:
                self.attrs.append(
                    (attr_id, StructSymbol(unit, self.scope, attr_node))
                )

            elif attr_type is DataAttr:
                self.attrs.append(
                    (attr_id, DataAttrSymbol(attr_node, attr_index))
                )
                attr_index += 1

            elif attr_type is ConstructOperNode:
                self.attrs.append(
                    (
                        attr_id,
                        ConstructOperSymbol(unit, self, attr_node, self.scope)
                    )
                )

            elif attr_type is DestructOperNode:
                self.attrs.append(
                    (
                        attr_id,
                        DestructOperSymbol(unit, self, attr_node, self.scope)
                    )
                )

            else:
                raise Todo()

    def get_ctor_symbol(self):
        for attr_id, attr_symbol in self.attrs:
            if attr_id == "construct":
                if type(attr_symbol) is ConstructOperSymbol:
                    return attr_symbol

        return None

    def get_dtor_symbol(self):
        for attr_id, attr_symbol in self.attrs:
            if attr_id == "destruct":
                if type(attr_symbol) is DestructOperSymbol:
                    return attr_symbol

        return None

    def get_attr_symbol(self, id):
        for attr_id, attr_symbol in self.attrs:
            if attr_id == id:
                if (
                    type(attr_symbol) is AttrFunSymbol or
                    type(attr_symbol) is DataAttrSymbol
                ):
                    return attr_symbol
                else:
                    raise Todo()

        raise Todo()

    def _on_ir(self, value):
        self._ir_value = value

    def get_ir_value(self):
        if self._ir_value is None:
            raise Todo()
        else:
            return self._ir_value
