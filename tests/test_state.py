from automata import State


def test_equality():
    assert State("q0") == State("q0")
    assert State("q0") != State("q1") != State("q2")
