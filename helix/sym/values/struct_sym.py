
from ...err import Todo
from ...ast import (
    DataAttr, FunNode, StructNode, ConstructOperNode, DestructOperNode
)

from ..scope import Scope

from .fun_sym import FunSym, AttrFunSym
from .oper_sym import ConstructOperSym, DestructOperSym

class DataAttrSym:
    def __init__(self, ast, index):
        self.ast = ast
        self.id = ast.id
        self.index = index

        self._ir_type = None
        self.type = None

    @property
    def ir_type(self):
        if self._ir_type is None:
            raise Todo()

        else:
            return self._ir_type

    @ir_type.setter
    def ir_type(self, t):
        self._ir_type = t

class StructSym:
    def __init__(self, unit, parent_scope, ast):
        from ...targets import StructTarget

        self.unit = unit
        self.parent_scope = parent_scope
        self.scope = Scope(parent_scope)
        self.ast = ast
        self.attrs = [ ]

        self.id = self.ast.id

        self.target = StructTarget(self)
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
                        AttrFunSym(
                            unit,
                            self,
                            attr_node.id,
                            attr_node,
                            self.scope,
                            is_mut = attr_node.is_mut
                        )
                    ))

                else:
                    self.attrs.append(
                        (attr_id, FunSym(unit, attr_node, self.scope))
                    )

            elif attr_type is StructNode:
                self.attrs.append(
                    (attr_id, StructSym(unit, self.scope, attr_node))
                )

            elif attr_type is DataAttr:
                self.attrs.append(
                    (attr_id, DataAttrSym(attr_node, attr_index))
                )
                attr_index += 1

            elif attr_type is ConstructOperNode:
                self.attrs.append(
                    (
                        attr_id,
                        ConstructOperSym(unit, self, attr_node, self.scope)
                    )
                )

            elif attr_type is DestructOperNode:
                self.attrs.append(
                    (
                        attr_id,
                        DestructOperSym(unit, self, attr_node, self.scope)
                    )
                )

            else:
                raise Todo()

    def get_ctor_symbol(self):
        for attr_id, attr_symbol in self.attrs:
            if attr_id == "construct":
                if type(attr_symbol) is ConstructOperSym:
                    return attr_symbol

        return None

    def get_dtor_symbol(self):
        for attr_id, attr_symbol in self.attrs:
            if attr_id == "destruct":
                if type(attr_symbol) is DestructOperSym:
                    return attr_symbol

        return None

    def get_attr_symbol(self, id):
        for attr_id, attr_symbol in self.attrs:
            if attr_id == id:
                if (
                    type(attr_symbol) is AttrFunSym or
                    type(attr_symbol) is DataAttrSym
                ):
                    return attr_symbol
                else:
                    raise Todo()

        raise Todo()

    @property
    def ir_value(self):
        return self.target.ir_value
