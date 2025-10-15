from minilisp.parser import parse_to_tree

def test_number():
    assert parse_to_tree("42") == [42]

def test_identifier():
    assert parse_to_tree("x") == ["x"]


