from minilisp.parser import parse_to_tree

exprs = [
    "( + 2 3 )",
    "( × ( + 1 2 ) 3 )",
    "( f 1 2 3 )",
    "( λ x x )",
    "( ≜ add ( λ x x ) y )",
]

for e in exprs:
    print("Input:", e)
    try:
        ast = parse_to_tree(e)
        print("AST:", ast)
    except Exception as ex:
        print("Error:", ex)
    print("---")
