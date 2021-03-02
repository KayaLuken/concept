from conc.interpreter import Interpreter


def test_echo():
    interpreter = Interpreter()
    interpreter.interpret("$ 2")

    assert interpreter.output == 2


def test_addition():
    interpreter = Interpreter()
    interpreter.interpret("$ 1 + 2")

    assert interpreter.output == 3


def test_tautology():
    interpreter = Interpreter()
    interpreter.interpret("$ 1 = 1")

    assert interpreter.output == True

def test_sentences():
    interpreter = Interpreter()
    interpreter.interpret("$ 2 ; $ 2 + 2")

    assert interpreter.output == [2, 4]
