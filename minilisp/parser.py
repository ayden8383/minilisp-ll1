from typing import List, Any
from .lexer import lex, Token
from .parse_table import TABLE, START_SYMBOL

class ParseError(Exception):
    pass

def parse_to_tree(src: str) -> Any:
    tokens = lex(src)
    # Standard LL(1) predictive parsing stack: [EOF, START_SYMBOL]
    stack: List[str] = ["EOF", START_SYMBOL]
    pos = 0

    # For building a simple tree, we’ll use a parallel node stack
    node_stack: List[Any] = []

    def lookahead_type() -> str:
        return tokens[pos].type

    while stack:
        top = stack.pop()
        la = lookahead_type()

        if top == "EOF":
            if la == "EOF":
                # Finished successfully; node_stack should contain exactly one tree.
                return node_stack.pop() if node_stack else None
            else:
                raise ParseError(f"Expected EOF but saw {la}")

        # Terminal?
        if top.isupper():  # convention: terminals are UPPERCASE token types
            if la == top:
                # consume token
                node_stack.append(token_to_node(tokens[pos]))
                pos += 1
            else:
                raise ParseError(f"Expected {top} but saw {la}")
            continue

        # Nonterminal: expand using table
        key = (top, la)
        if key not in TABLE:
            raise ParseError(f"No rule for ({top}, {la})")
        production = TABLE[key]

        # For building trees: push a marker to group children under this nonterminal
        node_stack.append(("NT", top, 0))  # 0 = number of children to attach next commit

        # Push RHS in reverse onto stack
        for sym in reversed(production):
            stack.append(sym)

        # Stash how many RHS symbols to expect
        node_stack[-1] = ("NT", top, len(production))

      

        # Perform reductions opportunistically:
        node_stack = reduce_nodes(node_stack)

    raise ParseError("Unexpected end of parse")

def token_to_node(tok: Token):
    if tok.type == "NUMBER":
        return int(tok.value)
    if tok.type == "IDENTIFIER":
        return tok.value
    # Map operators to readable names; parentheses don’t appear in final tree
    op_map = {
        "PLUS": "PLUS",
        "MINUS": "MINUS",
        "TIMES": "MULT",
        "EQUALS": "EQUALS",
        "QMARK": "IF",
        "LAMBDA": "LAMBDA",
        "DEF": "DEFINE",
    }
    if tok.type in op_map:
        return op_map[tok.type]
    if tok.type in ("LPAREN", "RPAREN", "EOF"):
        return None
    return tok.value

def reduce_nodes(stack):
    """
    Groups the last N concrete nodes under the last ('NT', name, N) marker.
    This is a minimal illustrative reducer to produce list-based trees.
    """
    if not stack:
        return stack
    if isinstance(stack[-1], tuple) and stack[-1][0] == "NT":
        nt, name, n = stack.pop()
        children = []
        # pull last n non-marker nodes
        while n > 0 and stack:
            node = stack.pop()
            if isinstance(node, tuple) and node and node[0] == "NT":
                # Nested marker encountered—push back and stop
                stack.append(node)
                break
            if node is not None:
                children.append(node)
            n -= 1
        children.reverse()
     
        stack.append(children)
    return stack
