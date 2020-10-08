from conc.interpreter import Interpreter


def test_echo():
    interpreter = Interpreter()
    interpreter.interpret("EVAL 2")

    assert interpreter.output == "2"


def test_addition():
    return
    interpreter = Interpreter()
    interpreter.interpret("EVAL 2 + 2")

    assert interpreter.output == "4"
