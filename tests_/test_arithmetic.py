from conc.interpreter import Interpreter


def test_echo():
    interpreter = Interpreter()
    interpreter.interpret("EVAL 2")

    assert interpreter.output == 2


def test_addition():
    interpreter = Interpreter()
    interpreter.interpret("EVAL 2 + 2")

    assert interpreter.output == 4


def test_tautology():
    interpreter = Interpreter()
    interpreter.interpret("EVAL 1 = 1")

    assert interpreter.output == True
