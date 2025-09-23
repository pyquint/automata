import pytest

from automata import State


@pytest.fixture(autouse=True)
def run_around_tests():
    State.reset_naming()
    yield
