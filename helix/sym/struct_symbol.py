
from ..err import Todo
from ..ast import (
    DataAttr, FunNode, StructNode, ConstructOperNode, DestructOperNode
)
from ..ir import StructType, gen_static_expr_ir

from .fun_symbol import FunSymbol, AttrFunSymbol
from .oper_symbol import ConstructOperSymbol, DestructOperSymbol

from .scope import Scope
from .target import Target

class StructTarget(Target):
    def __init__(self, symbol):
        super().__init__([ ])

        from ..sym import (
            DataAttrSymbol,
            AttrFunSymbol,
            ConstructOperSymbol,
            DestructOperSymbol
        )

        self.symbol = symbol
        self.attrs = { }

        self._ir_value = None

    @property
    def ir_value(self):
        if self._ir_value is not None:
            return self._ir_value

        else:
            raise Todo("struct has not been built yet")

    def build(self):
        from ..sym import DataAttrSymbol

        data = [ ]

        for attr_id, symbol in self.symbol.attrs:
            if type(symbol) is DataAttrSymbol:
                data.append(symbol)
                symbol.ir_type = gen_static_expr_ir(
                    self.symbol.parent_scope, symbol.ast.type
                )

        self._ir_value = StructType(
            self.attrs,
            [
                (
                    member.ir_type,
                    member.id
                )
                for member in
                data
            ]
        )

class DataAttrSymbol:
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

class StructSymbol:
    def __init__(self, unit, parent_scope, ast):
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

    @property
    def ir_value(self):
        return self.target.ir_value
