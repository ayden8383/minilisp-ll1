# tests/test_partA_analysis.py
import subprocess, sys, re

def run():
    return subprocess.check_output(
        [sys.executable, "-m", "minilisp.ll1_analyzer"], text=True
    )

def grab(line_prefix, out):
    return [ln for ln in out.splitlines() if ln.startswith(line_prefix)]

def test_first_sets_basic():
    out = run()
    assert "FIRST(program) = {" in out
    assert "FIRST(expr) = {" in out
    assert "FIRST(paren-expr) = {" in out

def test_follow_sets_basic():
    out = run()
    assert "FOLLOW(expr) = {" in out
    assert "FOLLOW(paren-expr) = {" in out

def test_parse_table_has_all_rows():
    out = run()
    # spot-check some rows
    assert "M[program    , NUMBER    ] = program -> expr" in out
    assert "M[expr       , LPAREN    ] = expr -> LPAREN paren-expr RPAREN" in out
    assert "M[paren-expr , PLUS      ] = paren-expr -> PLUS expr expr" in out
    # application form:
    assert "M[paren-expr , NUMBER    ] = paren-expr -> expr expr*" in out
