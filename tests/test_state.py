import pytest

from automata import State


def test_equality():
    assert State("q0") == State("q0")
    assert State("q0") != State("q1") != State("q2")


def test_non_string_name():
    with pytest.raises(TypeError):
        _ = State(1)  # pyright: ignore[reportArgumentType]
    with pytest.raises(TypeError):
        _ = State({})  # pyright: ignore[reportArgumentType]


def test_non_string_base_state_name():
    with pytest.raises(TypeError):
        State.set_base_name(1)  # pyright: ignore[reportArgumentType]


def test_auto_naming():
    assert State(f"{State.base_name}{State.instance_counter}") == State() == State("q0")
    assert State(f"{State.base_name}{State.instance_counter}") == State() == State("q1")
