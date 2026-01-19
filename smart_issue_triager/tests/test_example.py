from smart_issue_triager.logic import add


def test_add_success():
    assert add(1, 2) == 3


def test_add_negative():
    assert add(-1, 1) == 0
