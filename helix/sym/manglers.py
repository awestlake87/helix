
from ..err import Todo

def mangle_name(scoped_name, reserved=False):
    if not reserved:
        return mangle_scoped_name(scoped_name, "_M")
    else:
        return mangle_scoped_name(scoped_name, "_MR")

def mangle_vtable_name(scoped_name, reserved=False):
    if not reserved:
        return mangle_scoped_name(scoped_name, "_MV")
    else:
        return mangle_scoped_name(scoped_name, "_MRV")

def mangle_type_info_name(scoped_name, reserved=False):
    if not reserved:
        return mangle_scoped_name(scoped_name, "_MT")
    else:
        return mangle_scoped_name(scoped_name, "_MRT")



def demangle_name(mangled_name, reserved=False):
    if not reserved:
        return demangle_scoped_name(mangled_name, "_M")
    else:
        return demangle_scoped_name(mangled_name, "_MR")

def demangle_vtable_name(mangled_name, reserved=False):
    if not reserved:
        return demangle_scoped_name(mangled_name, "_MV")
    else:
        return demangle_scoped_name(mangled_name, "_MRV")

def demangle_type_info_name(mangled_name, reserved=False):
    if not reserved:
        return demangle_scoped_name(mangled_name, "_MT")
    else:
        return demangle_scoped_name(mangled_name, "_MRT")



def mangle_scoped_name(name_list, prefix="_M"):
    def mangle_part(part):
        mangled_part = ""

        for c in part:
            if (
                c >= 'a' and c <= 'z' or
                c >= 'A' and c <= 'Z' or
                c >= '0' and c <= '9' or
                c == '_'
            ):
                mangled_part += c

            else:
                raise Todo(c)

        return "{}{}".format(len(mangled_part), mangled_part)

    return "{}{}".format(
        prefix,
        "".join([ mangle_part(part) for part in name_list ])
    )

def demangle_scoped_name(name, prefix="_M"):
    def split_mangled_name():
        nonlocal name
        nonlocal prefix

        if len(name) < len(prefix) or name[0:len(prefix)] != prefix:
            raise Todo(name)

        i = len(prefix)

        length = ""
        while i < len(name):
            c = name[i]
            if c >= '0' and c <= '9':
                length += c
                i += 1

            else:
                if len(length) == 0:
                    raise Todo(name)

                length = int(length)

                yield name[i:(i + length)]

                i += length
                length = ""


    def demangle_part(part):
        demangled_part = ""

        for c in part:
            if (
                c >= 'a' and c <= 'z' or
                c >= 'A' and c <= 'Z' or
                c >= '0' and c <= '9' or
                c == '_'
            ):
                demangled_part += c

        return demangled_part

    return [ demangle_part(part) for part in split_mangled_name() ]
