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
pip install -r requirements.txt
pytest
