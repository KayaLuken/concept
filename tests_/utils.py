from contextlib import contextmanager

import pytest

from conc.interpreter import Interpreter


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail("DID RAISE {0}".format(exception))


def assert_outputs(expression, expected_output):
    interpreter = Interpreter()
    interpreter.interpret(expression)

    assert interpreter.output == expected_output, '{} != {}'.format(interpreter.output, expected_output)