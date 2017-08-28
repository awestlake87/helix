import unittest

from ..sym.manglers import *

class TestManglers(unittest.TestCase):
    def test_basic_mangling(self):
        scoped_name = [ "module", "unit", "Type12", "a_function" ]
        mangled_name = "_M6module4unit6Type1210a_function"

        self.assertEqual(
            mangled_name,
            mangle_name(scoped_name)
        )

        self.assertEqual(
            scoped_name,
            demangle_name(mangled_name)
        )

    def test_reserved_mangling(self):
        scoped_name = [ "todo" ]
        mangled_name = "_MR4todo"

        self.assertEqual(
            mangled_name,
            mangle_name(scoped_name, reserved=True)
        )

        self.assertEqual(
            scoped_name,
            demangle_name(mangled_name, reserved=True)
        )

    def test_rtti_mangling(self):
        scoped_name = [ "module", "unit", "Type", "function" ]
        vtable_name = "_MV6module4unit4Type8function"
        tinfo_name = "_MT6module4unit4Type8function"

        self.assertEqual(
            vtable_name,
            mangle_vtable_name(scoped_name)
        )

        self.assertEqual(
            tinfo_name,
            mangle_type_info_name(scoped_name)
        )

        self.assertEqual(
            scoped_name,
            demangle_vtable_name(vtable_name)
        )
        self.assertEqual(
            scoped_name,
            demangle_type_info_name(tinfo_name)
        )
