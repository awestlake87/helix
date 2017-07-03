

class Symbol:
    def is_unit(self):
        return False

    def is_struct(self):
        return False

    def is_fun(self):
        return False

    def can_overload(self):
        return Falses

    def get_call_deps(self, scope, args):
        return [ ]

    def get_target(self):
        return None

def mangle_qualified_name(name):
    return name
