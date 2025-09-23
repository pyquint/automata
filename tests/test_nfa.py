import pytest

from automata import NFA, State
from automata.nfa import epsilon


def test_non_string_input():
    test_dfa = NFA({q0 := State("q0")}, {"a"}, {q0: {"a": {q0}}}, {q0}, {q0})

    with pytest.raises(TypeError):
        _ = test_dfa.accepts(1)  # pyright: ignore[reportArgumentType]

    with pytest.raises(TypeError):
        _ = test_dfa.accepts({"a"})  # pyright: ignore[reportArgumentType]


def test_no_states():
    with pytest.raises(ValueError):
        _ = NFA(set(), {"a"}, {}, {q0 := State("q0")}, {q0})


def test_no_alphabet():
    with pytest.raises(ValueError):
        _ = NFA({q0 := State("q0")}, set(), {q0: {"a": {q0}}}, {q0}, {q0})


def test_alphabet_with_multilength_strings():
    with pytest.raises(ValueError):
        _ = NFA({q0 := State("q0")}, {"abc"}, {q0: {"a": {q0}}}, {q0}, {q0})


def test_transition_symbol_not_in_alphabet():
    with pytest.raises(ValueError):
        _ = NFA(
            {
                q0 := State("q0"),
            },
            {"a"},
            {q0: {"b": {q0}}},
            {q0},
            {q0},
        )


def test_rewrite_transition_duplicate_definition():
    test_nfa = NFA(
        {q0 := State("q0"), q1 := State("q1")},
        {"a", "b"},
        {q0: {"a": {q0}}, q0: {"b": {q1}}},
        {q0},
        {q0},
    )

    assert test_nfa.transitions == {q0: {"b": {q1}}}


def test_no_transitions():
    with pytest.raises(ValueError):
        _ = NFA({q0 := State("q0")}, {"a"}, {}, {q0}, {q0})


def test_incomplete_transition():
    ab_or_b = NFA(
        {q0 := State("q0"), q1 := State("q1"), q2 := State("q2")},
        {"a", "b"},
        {q0: {"a": {q1}, "b": {q2}}, q1: {"b": {q2}}},
        {q0},
        {q2},
    )

    assert ab_or_b.accepts("b")
    assert ab_or_b.accepts("ab")

    assert not ab_or_b.accepts("a")
    assert not ab_or_b.accepts("aa")
    assert not ab_or_b.accepts("abaaaa")


def test_no_accepting():
    test_nfa = NFA(
        {q0 := State("q0")},
        {"a"},
        {q0: {"a": {q0}}},
        {q0},
        set(),
    )

    assert test_nfa.accepting == set()


def test_unrecognized_accepting():
    test_nfa = NFA(
        {q0 := State("q0"), q1 := State("q1")},
        {"a"},
        {q0: {"a": {q0}}, q1: {"a": {q1}}},
        {q0},
        {q5 := State("q5")},
    )

    assert test_nfa.accepting == {q5}


def test_concat():
    a = NFA(
        {a1 := State("a1"), a2 := State("a2")},
        {"a"},
        {a1: {"a": {a2}}},
        {a1},
        {a2},
    )

    b = NFA(
        {b1 := State("b1"), b2 := State("b2")},
        {"b"},
        {b1: {"b": {b2}}},
        {b1},
        {b2},
    )

    ab = NFA.concat(a, b)

    assert ab.states == a.states | b.states
    assert ab.alphabet == a.alphabet | b.alphabet
    assert ab.initial == a.initial
    assert ab.accepting == b.accepting

    assert ab.delta(a1, "a") == {a2} == ab.transitions[a1]["a"]
    assert ab.delta(b1, "b") == {b2} == ab.transitions[b1]["b"]
    assert ab.delta(a2, epsilon) == {b1} == ab.transitions[a2][epsilon]


def test_union():
    a = NFA(
        {a1 := State("a1"), a2 := State("a2")},
        {"a"},
        {a1: {"a": {a2}}},
        {a1},
        {a2},
    )

    b = NFA(
        {b1 := State("b1"), b2 := State("b2")},
        {"b"},
        {b1: {"b": {b2}}},
        {b1},
        {b2},
    )

    a_or_b = NFA.union(a, b)

    new_initial = State(f"{State.base_name}{State.instance_counter - 2}")
    new_accepting = State(f"{State.base_name}{State.instance_counter - 1}")

    assert a_or_b.states == a.states | b.states | {new_initial, new_accepting}
    assert a_or_b.alphabet == a.alphabet | b.alphabet
    assert a_or_b.initial == {new_initial}
    assert a_or_b.accepting == {new_accepting}

    assert a_or_b.delta(a1, "a") == {a2} == a_or_b.transitions[a1]["a"]
    assert a_or_b.delta(b1, "b") == {b2} == a_or_b.transitions[b1]["b"]
    assert (
        a_or_b.delta(new_initial, epsilon)
        == {a1, b1}
        == a_or_b.transitions[new_initial][epsilon]
    )
    assert (
        a_or_b.delta(a2, epsilon) == {new_accepting} == a_or_b.transitions[a2][epsilon]
    )
    assert (
        a_or_b.delta(b2, epsilon) == {new_accepting} == a_or_b.transitions[b2][epsilon]
    )


def test_kleene_star():
    a = NFA(
        {a1 := State("a1"), a2 := State("a2")},
        {"a"},
        {a1: {"a": {a2}}},
        {a1},
        {a2},
    )

    a_star = NFA.kleene_star(a)

    new_initial = State(f"{State.base_name}{State.instance_counter - 2}")
    new_accepting = State(f"{State.base_name}{State.instance_counter - 1}")

    assert a_star.epsilon_closure({new_initial}) == {new_initial, a1, new_accepting}
    assert a_star.epsilon_closure({a2}) == {a1, a2, new_accepting}


def test_kleene_plus():
    a = NFA(
        {a1 := State("a1"), a2 := State("a2")},
        {"a"},
        {a1: {"a": {a2}}},
        {a1},
        {a2},
    )

    a_star = NFA.kleene_star(a, plus=True)

    new_initial = State(f"{State.base_name}{State.instance_counter - 2}")
    new_accepting = State(f"{State.base_name}{State.instance_counter - 1}")

    assert a_star.epsilon_closure({new_initial}) == {new_initial, a1}
    assert a_star.epsilon_closure({a2}) == {a1, a2, new_accepting}
