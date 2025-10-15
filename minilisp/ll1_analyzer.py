
from __future__ import annotations
from collections import defaultdict
from typing import Dict, List, Set
import sys, os

EPS = "ε"

Nonterm = str
Term = str
Symbol = str


class Grammar:
    def __init__(self, start: Nonterm):
        self.start: Nonterm = start
        self.productions: Dict[Nonterm, List[List[Symbol]]] = defaultdict(list)
        self.nonterms: Set[Nonterm] = set()
        self.terms: Set[Term] = set()

    def add(self, lhs: Nonterm, *rhs_alts: List[Symbol]) -> None:
        self.nonterms.add(lhs)
        for rhs in rhs_alts:
            self.productions[lhs].append(rhs)


def compute_first(G: Grammar) -> Dict[Symbol, Set[str]]:
    """Compute FIRST sets for all nonterminals (and terminals map to themselves)."""
    FIRST: Dict[Symbol, Set[str]] = defaultdict(set)

    # terminals: FIRST(t) = {t}
    for t in G.terms:
        FIRST[t].add(t)

    # epsilon for completeness
    FIRST[EPS].add(EPS)

    # ensure keys for nonterminals
    for A in G.nonterms:
        FIRST[A]  # create key

    changed = True
    while changed:
        changed = False
        for A, alts in G.productions.items():
            for alpha in alts:
                nullable_prefix = True
                for Y in alpha:
                    Fy = FIRST.get(Y, set())
                    before = len(FIRST[A])
                    FIRST[A].update(Fy - {EPS})
                    if len(FIRST[A]) != before:
                        changed = True
                    if EPS not in Fy:
                        nullable_prefix = False
                        break
             
                if nullable_prefix:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
    return FIRST


def first_of_sequence(seq: List[Symbol], FIRST: Dict[Symbol, Set[str]]) -> Set[str]:
    """FIRST of a sequence; always returns a set. Empty seq => {ε}."""
    out: Set[str] = set()
    if not seq:
        return {EPS}

    nullable_prefix = True
    for Y in seq:
        Fy = FIRST.get(Y, set())
        out.update(Fy - {EPS})
        if EPS not in Fy:
            nullable_prefix = False
            break

    if nullable_prefix:
        out.add(EPS)
    return out


def compute_follow(G: Grammar, FIRST: Dict[Symbol, Set[str]]) -> Dict[Nonterm, Set[str]]:
    """Compute FOLLOW sets for all nonterminals."""
    FOLLOW: Dict[Nonterm, Set[str]] = defaultdict(set)
    FOLLOW[G.start].add("EOF")

    changed = True
    while changed:
        changed = False
        for A, alts in G.productions.items():
            for alpha in alts:
                for i, B in enumerate(alpha):
                    if B not in G.nonterms:
                        continue
                    beta = alpha[i + 1 :]

                    if beta:
                        first_beta = first_of_sequence(beta, FIRST)
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(first_beta - {EPS})
                        if len(FOLLOW[B]) != before:
                            changed = True

                        if EPS in first_beta:
                            before = len(FOLLOW[B])
                            FOLLOW[B].update(FOLLOW[A])
                            if len(FOLLOW[B]) != before:
                                changed = True
                    else:
                        # B is at end of the production
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(FOLLOW[A])
                        if len(FOLLOW[B]) != before:
                            changed = True
    return FOLLOW


def _enable_utf8_stdout():
    try:

        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def formatted_set(s: Set[str]) -> str:

    items = []
    for x in sorted(s, key=lambda x: (x == EPS, x)):
        if x == EPS and os.name == "nt":
            items.append("EPS")
        else:
            items.append(x)
    text = "{" + ", ".join(items) + "}"
    return text


def build_grammar() -> Grammar:
    """Part A grammar with expr* desugared as ARGS for computation."""
    G = Grammar(start="program")

    # program -> expr
    G.add("program", ["expr"])

    # expr -> NUMBER | IDENTIFIER | LPAREN paren-expr RPAREN
    G.add(
        "expr",
        ["NUMBER"],
        ["IDENTIFIER"],
        ["LPAREN", "paren-expr", "RPAREN"],
    )

    # paren-expr -> operator-led | expr expr*
    G.add(
        "paren-expr",
        ["PLUS", "expr", "expr"],
        ["TIMES", "expr", "expr"],
        ["EQUALS", "expr", "expr"],
        ["MINUS", "expr", "expr"],
        ["QMARK", "expr", "expr", "expr"],
        ["LAMBDA", "IDENTIFIER", "expr"],
        ["DEF", "IDENTIFIER", "expr", "expr"],
        ["expr", "ARGS"],  # desugared expr*
    )

    # ARGS -> expr ARGS | ε
    G.add("ARGS", ["expr", "ARGS"], [EPS])

    # Terminals (token types)
    G.terms.update(
        {
            "NUMBER",
            "IDENTIFIER",
            "LPAREN",
            "RPAREN",
            "PLUS",
            "MINUS",
            "TIMES",
            "EQUALS",
            "QMARK",
            "LAMBDA",
            "DEF",
            "EOF",
        }
    )
    return G


def print_results():
    _enable_utf8_stdout()
    G = build_grammar()
    FIRST = compute_first(G)
    FOLLOW = compute_follow(G, FIRST)

    print("== FIRST sets ==")
    for A in ["program", "expr", "paren-expr", "ARGS"]:
        print(f"FIRST({A}) = {formatted_set(FIRST[A])}")
    print()

    print("== FOLLOW sets ==")
    for A in ["program", "expr", "paren-expr", "ARGS"]:
        print(f"FOLLOW({A}) = {formatted_set(FOLLOW[A])}")
    print()

    print("== LL(1) Parse Table (human-readable for Part A) ==")

    def row(nt: str, lookaheads: List[str], prod: List[str]):
        for a in lookaheads:
            print(f"M[{nt:11s}, {a:10s}] = {nt} -> {' '.join(prod)}")

    # program
    row("program", ["NUMBER", "IDENTIFIER", "LPAREN"], ["expr"])

    # expr
    row("expr", ["NUMBER"], ["NUMBER"])
    row("expr", ["IDENTIFIER"], ["IDENTIFIER"])
    row("expr", ["LPAREN"], ["LPAREN", "paren-expr", "RPAREN"])

    # paren-expr — operator-led forms
    row("paren-expr", ["PLUS"], ["PLUS", "expr", "expr"])
    row("paren-expr", ["TIMES"], ["TIMES", "expr", "expr"])
    row("paren-expr", ["EQUALS"], ["EQUALS", "expr", "expr"])
    row("paren-expr", ["MINUS"], ["MINUS", "expr", "expr"])
    row("paren-expr", ["QMARK"], ["QMARK", "expr", "expr", "expr"])
    row("paren-expr", ["LAMBDA"], ["LAMBDA", "IDENTIFIER", "expr"])
    row("paren-expr", ["DEF"], ["DEF", "IDENTIFIER", "expr", "expr"])

    # paren-expr — application form: starts with FIRST(expr)
    row("paren-expr", ["NUMBER", "IDENTIFIER", "LPAREN"], ["expr", "expr*"])


if __name__ == "__main__":
    print_results()
