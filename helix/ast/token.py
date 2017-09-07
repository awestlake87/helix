

class Token:
    NONE                = "NONE"

    END                 = "END"
    INDENT              = "INDENT"
    DEDENT              = "DEDENT"
    NODENT              = "NODENT"

    ID                  = "ID"
    ATTR_ID             = "ATTR_ID"

    KW_CFUN             = "cfun"
    KW_CGLOBAL          = "cglobal"
    KW_VARGS            = "vargs"

    KW_FUN              = "fun"
    KW_OPER             = "oper"
    KW_GLOBAL           = "global"
    KW_STRUCT           = "struct"

    KW_SWITCH           = "switch"
    KW_CASE             = "case"
    KW_DEFAULT          = "default"

    KW_IF               = "if"
    KW_ELIF             = "elif"
    KW_ELSE             = "else"
    KW_THEN             = "then"

    KW_FOR              = "for"
    KW_WHILE            = "while"
    KW_EACH             = "each"
    KW_LOOP             = "loop"
    KW_UNTIL            = "until"
    KW_BREAK            = "break"
    KW_CONTINUE         = "continue"

    KW_TRY              = "try"
    KW_CATCH            = "catch"
    KW_THROW            = "throw"
    KW_EXCEPT           = "except"
    KW_NOTHROW          = "nothrow"

    KW_IMPORT           = "import"
    KW_EXPORT           = "export"
    KW_LINK             = "link"
    KW_FROM             = "from"

    KW_PASS             = "pass"
    KW_RETURN           = "return"

    KW_DO               = "do"

    KW_VOID             = "void"
    KW_AUTO             = "auto"
    KW_MUT              = "mut"

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

    OP_L_EMBED          = "embed_<"
    OP_R_EMBED          = "embed_>"

    OP_RANGE            = ".."
    OP_SPREAD           = "..."

    OP_ADD_ASSIGN       = "+="
    OP_SUB_ASSIGN       = "-="
    OP_MUL_ASSIGN       = "*="
    OP_DIV_ASSIGN       = "/="
    OP_MOD_ASSIGN       = "%="

    OP_AND_ASSIGN       = "&="
    OP_XOR_ASSIGN       = "^="
    OP_OR_ASSIGN        = "|="
    OP_SHL_ASSIGN       = "<<="
    OP_SHR_ASSIGN       = ">>="

    OP_INC              = "++"
    OP_DEC              = "--"
    OP_LEQ              = "<="
    OP_GEQ              = ">="
    OP_SHL              = "<<"
    OP_SHR              = ">>"
    OP_EQ               = "=="
    OP_NEQ              = "!="

    OP_AND              = "and"
    OP_XOR              = "xor"
    OP_OR               = "or"
    OP_NOT              = "not"

    OP_AS               = "as"
    OP_CAST             = "cast"
    OP_BITCAST          = "bitcast"
    OP_SIZEOF           = "sizeof"
    OP_OFFSETOF         = "offsetof"
    OP_TYPEOF           = "typeof"

    OP_CONSTRUCT        = "@construct"
    OP_DESTRUCT         = "@destruct"

    LT_INT_BIN          = "int_x2"
    LT_INT_DEC          = "int_x10"
    LT_INT_HEX          = "int_x16"

    LT_CHAR             = "lt_char"
    LT_STRING           = "lt_string"

    LT_TRUE             = "true"
    LT_FALSE            = "false"
    LT_NIL              = "nil"


    def __init__(self, id, value=None):
        self.id = id
        self.value = value

    def _get_id_name(self):
        if type(self.id) is str:
            return "'{}'".format(self.id)
        else:
            return "unknown"

    def __repr__(self):
        if self.value != None:
            return "[{}({})]".format(self._get_id_name(), self.value)
        else:
            return "[{}]".format(self._get_id_name())
