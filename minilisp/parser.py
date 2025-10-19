from typing import List, Any, Optional
from .lexer import lex, Token

class ParseError(Exception):
    pass


def __parser_kind__() -> str:
    return "recursive-descent"

# -------- core parser --------

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    # -- basic token helpers --
    def la(self) -> str:
        return self.tokens[self.pos].type

    def cur(self) -> Token:
        return self.tokens[self.pos]

    def at(self, ttype: str) -> bool:
        return self.la() == ttype

    def eat(self, ttype: str) -> Token:
        if self.la() != ttype:
            raise ParseError(f"Expected {ttype} but saw {self.la()}")
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    # -- grammar: program -> expr EOF --
    def parse_program(self) -> Any:
        node = self.parse_expr()
        self.eat("EOF")
        return node

    # expr -> NUMBER | IDENTIFIER | LPAREN paren-expr RPAREN
    def parse_expr(self) -> Any:
        la = self.la()
        if la == "NUMBER":
            return self.num_node(self.eat("NUMBER"))
        if la == "IDENTIFIER":
            return self.id_node(self.eat("IDENTIFIER"))
        if la == "LPAREN":
            self.eat("LPAREN")
            node = self.parse_paren_expr()
            self.eat("RPAREN")
            return node
        raise ParseError(f"No rule for expr with lookahead {la}")

    # paren-expr -> operator-led | expr expr*
    def parse_paren_expr(self) -> Any:
        la = self.la()

        # operator-led (prefix) cases
        if la in ("PLUS", "MINUS", "TIMES", "EQUALS"):
            op = self.op_name(self.eat(la))
            a = self.parse_expr()
            b = self.parse_expr()
            return [op, a, b]

        if la == "QMARK":
            self.eat("QMARK")
            cnd = self.parse_expr()
            thn = self.parse_expr()
            els = self.parse_expr()
            return ["IF", cnd, thn, els]

        if la == "LAMBDA":
            self.eat("LAMBDA")
            name = self.id_node(self.eat("IDENTIFIER"))
            body = self.parse_expr()
            return ["LAMBDA", name, body]

        if la == "DEF":
            self.eat("DEF")
            name = self.id_node(self.eat("IDENTIFIER"))
            v1 = self.parse_expr()
            v2 = self.parse_expr()
            return ["DEFINE", name, v1, v2]

        func = self.parse_expr()
        args: List[Any] = []
        while self.la() in ("NUMBER", "IDENTIFIER", "LPAREN"):
            args.append(self.parse_expr())
        if args:
            return [func] + args
        return func

    # -- leaf makers / mapping --
    def num_node(self, tok: Token) -> int:
        return int(tok.value)

    def id_node(self, tok: Token) -> str:
        return tok.value

    def op_name(self, tok: Token) -> str:
        # Map lexer token types to AST operator names
        return {
            "PLUS": "PLUS",
            "MINUS": "MINUS",
            "TIMES": "MULT",
            "EQUALS": "EQUALS",
        }[tok.type]


def parse_to_tree(src: str) -> Any:
    tokens = lex(src)
    parser = Parser(tokens)
    return parser.parse_program()
