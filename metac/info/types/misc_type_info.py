
class AutoTypeInfo:
    pass

class VoidTypeInfo:
    pass

class IntTypeInfo:
    def __init__(self, num_bits, is_signed):
        self.num_bits = num_bits
        self.is_signed = is_signed

class FunTypeInfo:
    def __init__(self, ret_type, param_types):
        self.ret_type = ret_type
        self.param_types = param_types

class ArrayTypeInfo:
    pass
