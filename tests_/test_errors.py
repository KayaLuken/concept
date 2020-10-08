import pytest

from conc.interpreter import Interpreter


def test_addition():
    with pytest.raises(SyntaxError):
        interpreter = Interpreter()
        interpreter.interpret("EVAL 2 2")
