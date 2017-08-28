
from .scope import Scope

from ..err import Todo
from ..dep import StructTarget

from ..ast import DataAttr, FunNode, StructNode
from .fun_symbol import FunSymbol, AttrFunSymbol


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

            else:
                raise Todo()


        self._target = None
        self._ir_value = None

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

    def get_target(self):
        if self._target is None:
            self._target = StructTarget(self, on_ir=self._on_ir)

        return self._target

    def get_ir_value(self):
        if self._ir_value is None:
            raise Todo()
        else:
            return self._ir_value
