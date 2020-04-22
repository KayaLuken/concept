import pytest

from ..concepts import Obj, Int

foo = 3

@pytest.fixture
def x(): return Obj('x')

@pytest.fixture
def y(): return Obj('y')

@pytest.fixture
def a(): return Obj('a')

@pytest.fixture
def b(): return Obj('b')


@pytest.fixture
def five(): return Int('5')




