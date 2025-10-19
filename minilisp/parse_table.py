# Parse table skeleton.  will fill this using docs/ANALYSIS.md.
# Map: (NONTERM, lookahead_token_type) -> production as list of symbols (terminals/nonterminals)

NONTERMS = {"program", "expr", "paren-expr", "ARGS"}

# Terminals are token types from the lexer: NUMBER, IDENTIFIER, LPAREN, PLUS, MINUS, TIMES, EQUALS, QMARK, LAMBDA, DEF, RPAREN, EOF

TABLE = {
("program", "NUMBER"): ["expr"],
    ("program", "IDENTIFIER"): ["expr"],
    ("program", "LPAREN"): ["expr"],

    ("expr", "NUMBER"): ["NUMBER"],
    ("expr", "IDENTIFIER"): ["IDENTIFIER"],
    ("expr", "LPAREN"): ["LPAREN", "paren-expr", "RPAREN"],

    ("paren-expr", "PLUS"): ["PLUS", "expr", "expr"],
    ("paren-expr", "MINUS"): ["MINUS", "expr", "expr"],
    ("paren-expr", "TIMES"): ["TIMES", "expr", "expr"],
    ("paren-expr", "EQUALS"): ["EQUALS", "expr", "expr"],
    ("paren-expr", "QMARK"): ["QMARK", "expr", "expr", "expr"],
    ("paren-expr", "LAMBDA"): ["LAMBDA", "IDENTIFIER", "expr"],
    ("paren-expr", "DEF"): ["DEF", "IDENTIFIER", "expr", "expr"],

    ("paren-expr", "NUMBER"): ["expr", "ARGS"],
    ("paren-expr", "IDENTIFIER"): ["expr", "ARGS"],
    ("paren-expr", "LPAREN"): ["expr", "ARGS"],

    ("ARGS", "NUMBER"): ["expr", "ARGS"],
    ("ARGS", "IDENTIFIER"): ["expr", "ARGS"],
    ("ARGS", "LPAREN"): ["expr", "ARGS"],
  
    ("ARGS", "RPAREN"): [],
    ("ARGS", "EOF"): [],
}

START_SYMBOL = "program"
