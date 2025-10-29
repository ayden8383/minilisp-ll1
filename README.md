# MiniLisp LL(1) — Team Workspace (Python)


## Structure
- `docs/ANALYSIS.md` — theory notes (FIRST/FOLLOW, parse table)
- `minilisp/` — code (lexer, parser, CLI)
- `tests/` — unit tests

## Quickstart
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
cd minilisp-ll1
pip install -r requirements.txt
pytest
