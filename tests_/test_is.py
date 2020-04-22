from conc.interpreter import Interpreter
from conc.main import interpret
from ..const import ERROR_MESSAGE_PREFIX, TRUE



def test_echo():
    interpreter = Interpreter()
    interpreter.interpret("DEF x")

    assert interpreter.graph == "x"
    assert interpreter.output == "x"


# def test_tautology():
#     assert interpret("x IS x") == TRUE
