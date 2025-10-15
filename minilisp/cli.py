import sys
from .parser import parse_to_tree, ParseError

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m minilisp.cli \"( + 2 3 )\"")
        sys.exit(1)
    src = sys.argv[1]
    try:
        tree = parse_to_tree(src)
        print(tree)
    except ParseError as e:
        print(f"Parse error: {e}")
        sys.exit(2)
    except SyntaxError as e:
        print(f"Lex error: {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
