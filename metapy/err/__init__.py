
class CompilerBug(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class Todo(Exception):
    def __init__(self, msg=None):
        if msg == None:
            super().__init__("todo")
        else:
            super().__init__("todo: {}".format(msg))

class NotApplicable(Exception):
    def __init__(self, msg=None):
        if msg == None:
            super().__init__("not applicable")
        else:
            super().__init__("not applicable: {}".format(msg))

class UnexpectedChar(Exception):
    def __init__(self, c):
        super().__init__("unexpected char '{}'".format(c))

class ExpectedToken(Exception):
    def __init__(self, expected, got):
        super().__init__("expected {} got {}".format(expected, got))

class UnexpectedToken(Exception):
    def __init__(self, unexpected):
        super().__init__("unexpected {}".format(unexpected))

class ReturnTypeMismatch(Exception):
    def __init__(self):
        super().__init__("return value does not match expected type")

class NoImplicitCast(Exception):
    def __init__(self):
        super().__init__("no implicit cast exists for these types")


class SymbolNotFound(Exception):
    def __init__(self, id):
        super().__init__(
            "symbol \"{}\" not found in the current scope".format(id)
        )

class SymbolAlreadyExists(Exception):
    def __init__(self, id):
        super().__init__(
            "symbol \"{}\" already exists in the current scope".format(id)
        )
