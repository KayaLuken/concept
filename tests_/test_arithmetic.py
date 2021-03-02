from tests_.utils import assert_outputs


def test_echo():
    assert_outputs("$ 2", 2)

def test_addition():
    assert_outputs("$ 1 + 2", 3)

def test_tautology():
    assert_outputs("$ 1 = 1", True)

def test_sentences():
    assert_outputs("$ 2 ; $ 2 + 2", [2, 4])
