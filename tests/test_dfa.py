import pytest

from automata import DFA, State


def test_non_string_input():
    test_dfa = DFA({q0 := State("q0")}, {"a"}, {q0: {"a": q0}}, q0, {q0})

    with pytest.raises(TypeError):
        _ = test_dfa.accepts(1)  # pyright: ignore[reportArgumentType]

    with pytest.raises(TypeError):
        _ = test_dfa.accepts({"a"})  # pyright: ignore[reportArgumentType]


def test_no_states():
    with pytest.raises(ValueError):
        _ = DFA(set(), {"a"}, {}, q0 := State("q0"), {q0})


def test_no_alphabet():
    with pytest.raises(ValueError):
        _ = DFA({q0 := State("q0")}, set(), {q0: {"a": q0}}, q0, {q0})


def test_alphabet_with_multilength_strings():
    with pytest.raises(ValueError):
        _ = DFA({q0 := State("q0")}, {"abc"}, {q0: {"a": q0}}, q0, {q0})


def test_transition_symbol_not_in_alphabet():
    with pytest.raises(ValueError):
        _ = DFA(
            {
                q0 := State("q0"),
            },
            {"a"},
            {q0: {"b": q0}},
            q0,
            {q0},
        )


def test_rewrite_transition_duplicate_definition():
    test_dfa = DFA(
        {q0 := State("q0"), q1 := State("q0")},
        {"a", "b"},
        {q0: {"a": q0}, q0: {"b": q1}},
        q0,
        {q0},
    )

    assert test_dfa.transitions == {q0: {"b": q1}}


def test_no_transitions():
    with pytest.raises(ValueError):
        _ = DFA({q0 := State("q0")}, {"a"}, {}, q0, {q0})


def test_incomplete_transition():
    ab_or_b = DFA(
        {q0 := State("q0"), q1 := State("q1"), q2 := State("q2")},
        {"a", "b"},
        {q0: {"a": q1, "b": q2}, q1: {"b": q2}},
        q0,
        {q2},
    )

    assert ab_or_b.accepts("b")
    assert ab_or_b.accepts("ab")

    assert not ab_or_b.accepts("a")
    assert not ab_or_b.accepts("aa")
    assert not ab_or_b.accepts("abaaaa")


def test_no_accepting():
    test_dfa = DFA(
        {q0 := State("q0")},
        {"a"},
        {q0: {"a": q0}},
        q0,
        set(),
    )

    assert test_dfa.accepting == set()


def test_unrecognized_accepting():
    test_dfa = DFA(
        {q0 := State("q0"), q1 := State("q1")},
        {"a"},
        {q0: {"a": q0}, q1: {"a": q1}},
        q0,
        {q5 := State("q5")},
    )

    assert test_dfa.accepting == {q5}
