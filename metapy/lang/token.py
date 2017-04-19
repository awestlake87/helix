

class Token:
    NONE                = "NONE"

    END                 = "END"
    INDENT              = "INDENT"
    DEDENT              = "DEDENT"
    NODENT              = "NODENT"

    ID                  = "ID"

    KW_EXTERN           = "extern"
    KW_INTERN           = "intern"

    KW_FUN              = "fun"
    KW_GLOBAL           = "global"
    KW_STRUCT           = "struct"

    KW_SWITCH           = "switch"
    KW_CASE             = "case"
    KW_DEFAULT          = "default"

    KW_IF               = "if"
    KW_ELIF             = "elif"
    KW_ELSE             = "else"
    KW_THEN             = "then"

    KW_PASS             = "pass"
    KW_RETURN           = "return"

    KW_DO               = "do"

    KW_BIT              = "bit"
    KW_CHAR             = "char"

    KW_BYTE             = "byte"
    KW_SHORT            = "short"
    KW_INT              = "int"
    KW_LONG             = "long"

    KW_UBYTE            = "ubyte"
    KW_USHORT           = "ushort"
    KW_UINT             = "uint"
    KW_ULONG            = "ulong"

    OP_RANGE            = "'..'"
    OP_SPREAD           = "'...'"
    OP_UPSERT           = "':='"

    LT_INT_DEC          = "int10"
    LT_TRUE             = "true"
    LT_FALSE            = "false"
    LT_NIL              = "nil"


    def __init__(self, id, value=None):
        self.id = id
        self.value = value

    def _get_id_name(self):
        ids = {
            Token.END:              "END",
            Token.INDENT:           "INDENT",
            Token.DEDENT:           "DEDENT",
            Token.NODENT:           "NODENT",

            Token.ID:               "ID",

            Token.KW_EXTERN:        "extern",
            Token.KW_INTERN:        "intern",

            Token.KW_FUN:           "fun",
            Token.KW_GLOBAL:        "global",
            Token.KW_STRUCT:        "struct",

            Token.KW_SWITCH:        "switch",
            Token.KW_CASE:          "case",
            Token.KW_DEFAULT:       "default",

            Token.KW_IF:            "if",
            Token.KW_ELIF:          "elif",
            Token.KW_ELSE:          "else",
            Token.KW_THEN:          "then",

            Token.KW_PASS:          "pass",
            Token.KW_RETURN:        "return",

            Token.KW_BIT:           "bit",
            Token.KW_CHAR:          "char",

            Token.KW_BYTE:          "byte",
            Token.KW_SHORT:         "short",
            Token.KW_INT:           "int",
            Token.KW_LONG:          "long",

            Token.KW_UBYTE:         "ubyte",
            Token.KW_USHORT:        "ushort",
            Token.KW_UINT:          "uint",
            Token.KW_ULONG:         "ulong",

            Token.OP_RANGE:         "..",
            Token.OP_SPREAD:        "...",
            Token.OP_UPSERT:        ":=",

            Token.LT_INT_DEC:       "int",
            Token.LT_TRUE:          "true",
            Token.LT_FALSE:         "false",
            Token.LT_NIL:           "nil"
        }

        if self.id in ids:
            return ids[self.id]
        elif type(self.id) is str:
            return "'{}'".format(self.id)
        else:
            return "unknown"

    def __repr__(self):
        if self.value != None:
            return "[{}({})]".format(self._get_id_name(), self.value)
        else:
            return "[{}]".format(self._get_id_name())
