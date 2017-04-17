

class Token:
    NONE                = 0
    END                 = 1
    INDENT              = 2
    DEDENT              = 3
    NODENT              = 4

    ID                  = 5
    
    KW_EXTERN           = 6
    KW_INTERN           = 7

    KW_FUN              = 8
    KW_GLOBAL           = 9
    KW_STRUCT           = 10

    KW_SWITCH           = 11
    KW_CASE             = 12
    KW_DEFAULT          = 13

    KW_IF               = 14
    KW_ELIF             = 15
    KW_ELSE             = 16
    KW_THEN             = 17

    KW_PASS             = 18
    KW_RETURN           = 19

    KW_BIT              = 20
    KW_CHAR             = 25
    
    KW_BYTE             = 21
    KW_SHORT            = 22
    KW_INT              = 23
    KW_LONG             = 24

    KW_UBYTE            = 26
    KW_USHORT           = 27
    KW_UINT             = 28
    KW_ULONG            = 29
    

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
            Token.KW_ULONG:         "ulong"
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

