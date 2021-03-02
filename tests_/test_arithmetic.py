from tests_.utils import assert_outputs


def test_echo():
    assert_outputs("$ 2", 2)

def test_addition():
    assert_outputs("$ 1 + 2", 3)

def test_tautology_1():
    assert_outputs("$ 1 = 1", True)

def test_sentences():
    assert_outputs("$ 2 ; $ 2 + 2", [2, 4])

def test_tautology_x():
    assert_outputs("$ x = x", True)
