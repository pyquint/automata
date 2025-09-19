from automata import NFA, State, epsilon


def test_closure_function():
    nfa_test = NFA(
        {
            q0 := State("0"),
            q1 := State("q1"),
            q2 := State("q2"),
        },
        {"a", "b"},
        {
            q0: {epsilon: {q1, q2}},
            q1: {},
            q2: {epsilon: {q1}},
        },
        {q0},
        {q2},
    )

    assert nfa_test.epsilon_closure({q0}) == {q0, q1, q2}
    assert nfa_test.epsilon_closure({q1}) == {q1}
    assert nfa_test.epsilon_closure({q2}) == {q1, q2}
    assert nfa_test.epsilon_closure({q0, q2}) == {q0, q1, q2}
