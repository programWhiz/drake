from rply import LexerGenerator

gen = LexerGenerator()

gen.ignore(r"\#.*\n")

gen.add("STR_TRIPLE_SINGLE", r"[rf]?'''[^'\\]*(?:(?:\\.|'(?!''))[^'\\]*)*'''")
gen.add("STR_TRIPLE_DOUBLE", r'[rf]?"""[^"\\]*(?:(?:\\.|"(?!""))[^"\\]*)*"""')
gen.add("STR_SINGLE_SINGLE", r"[rf]?'[^'\\]*(?:\\.[^'\\]*)*'")
gen.add("STR_SINGLE_DOUBLE", r'[rf]?"[^"\\]*(?:\\.[^"\\]*)*"')

gen.add("FLOAT", r"\-?((\d*\.\d+)|(\d+\.\d*))([eE]\-?\d[\d_]*)?")
gen.add("INTEGER", r"\-?\d[\d_]*")
gen.add("HEX_INT", r'0[xX](?:_?[0-9a-fA-F])+')
gen.add("BIN_INT", r'0[bB](?:_?[01])+')
gen.add("OCT_INT", r'0[oO](?:_?[0-7])+')
gen.add("DEC_INT", r'(?:0(?:_?0)*|[1-9](?:_?[0-9])*)')

gen.add("CLASS", "class")
gen.add("DEF", "def")
gen.add("AND", "and")
gen.add("NOT", "not")
gen.add("OR", "or")
gen.add("IF", "if")
gen.add("ELSE", "else")
gen.add("ELIF", "elif")
gen.add("IMPORT", "import")
gen.add("FROM", "from")
gen.add("RETURN", "return")
gen.add("YIELD", "return")
gen.add("BREAK", "break")
gen.add("PASS", "pass")
gen.add("DO", "do")
gen.add("WHILE", "while")
gen.add("FOR", "for")
gen.add("CONTINUE", "continue")
gen.add("COLON", ":")
gen.add("SEMICOLON", ";")

gen.add("WORD", "[a-zA-Z_]\w*")
gen.add("OPEN_PAREN", r"\(")
gen.add("CLOSE_PAREN", r"\)")
gen.add("COMMA", r"\,")
gen.add("DBL_EQ", "==")
gen.add("LE", "<=")
gen.add("GE", ">=")
gen.add("PLUS_EQ", r"\+=")
gen.add("MINUS_EQ", r"\-=")
gen.add("TIMES_EQ", r"\*=")
gen.add("DBL_DIV_EQ", r"\/\/=")
gen.add("DIV_EQ", r"\/=")
gen.add("MOD_EQ", r"\%=")
gen.add("DBL_AMP_EQ", r"\&\&=")
gen.add("DBL_PIPE_EQ", r"\|\|=")
gen.add("TILDE_EQ", r"\~=")
gen.add("PIPE_EQ", r"\|=")
gen.add("AMP_EQ", r"\&=")
gen.add("DBL_AMP", r"\&\&")
gen.add("DBL_PIPE", r"\|\|")
gen.add("EQ", "=")
gen.add("LT", "<")
gen.add("GT", ">")
gen.add("PLUS", r"\+")
gen.add("DASH", r"\-")
gen.add("ASTER", r"\*")
gen.add("DBL_FSLASH", r"\/\/")
gen.add("FSLASH", r"\/")
gen.add("BSLASH", r"\\")
gen.add("PERCENT", r"\%")
gen.add("AMP", r"\&")
gen.add("PIPE", r"\|")
gen.add("TILDE", r"\~")
gen.add("DOT", r"\.")

gen.add("NEWLINE", r"\n")
gen.add("SPACE", r"[ \t]+")

lexer = gen.build()