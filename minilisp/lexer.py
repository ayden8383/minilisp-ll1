import re
from dataclasses import dataclass
from typing import List, Iterator, Tuple

# Tokens: NUMBER, IDENTIFIER, LPAREN, RPAREN, PLUS, MINUS, TIMES, EQUALS, QMARK, LAMBDA, DEF, EOF

SYMBOLS = {
    "(": "LPAREN",
    ")": "RPAREN",
    "+": "PLUS",
    "−": "MINUS",   
    "×": "TIMES",
    "=": "EQUALS",
    "?": "QMARK",
    "λ": "LAMBDA",
    "≜": "DEF",
}

IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
NUM_RE = re.compile(r"\d+")

@dataclass
class Token:
    type: str
    value: str
    pos: int

def lex(src: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    n = len(src)

    while i < n:
        c = src[i]

        if c.isspace():
            i += 1
            continue

        if c in SYMBOLS:
            tokens.append(Token(SYMBOLS[c], c, i))
            i += 1
            continue

        m = NUM_RE.match(src, i)
        if m:
            tokens.append(Token("NUMBER", m.group(), i))
            i = m.end()
            continue

        m = IDENT_RE.match(src, i)
        if m:
            tokens.append(Token("IDENTIFIER", m.group(), i))
            i = m.end()
            continue

        raise SyntaxError(f"Illegal character '{c}' at {i}")

    tokens.append(Token("EOF", "", n))
    return tokens
