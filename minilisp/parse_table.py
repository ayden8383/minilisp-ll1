# Parse table skeleton.  will fill this using docs/ANALYSIS.md.
# Map: (NONTERM, lookahead_token_type) -> production as list of symbols (terminals/nonterminals)

NONTERMS = {"program", "expr", "paren-expr"}

# Terminals are token types from the lexer: NUMBER, IDENTIFIER, LPAREN, PLUS, MINUS, TIMES, EQUALS, QMARK, LAMBDA, DEF, RPAREN, EOF

TABLE = {
    # Example shape (not real values):
    # ("program", "NUMBER"): ["expr"],
    # ("expr", "NUMBER"): ["NUMBER"],
    # ("expr", "IDENTIFIER"): ["IDENTIFIER"],
    # ("expr", "LPAREN"): ["LPAREN", "paren-expr", "RPAREN"],
    # ("paren-expr", "PLUS"): ["PLUS", "expr", "expr"],
    # ...
}

START_SYMBOL = "program"
