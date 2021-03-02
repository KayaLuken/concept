import pytest

from conc.interpreter import Interpreter


def test_unconsumed_concept():
    with pytest.raises(SyntaxError):
        interpreter = Interpreter()
        interpreter.interpret("EVAL 2 2")
