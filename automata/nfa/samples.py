from automata import NFA, State, epsilon

A_OR_B_WHOLE_STAR = NFA(
    {
        s0 := State("s0"),
        q0 := State("q0"),
        q1 := State("q1"),
        q2 := State("q2"),
        q3 := State("q3"),
        q4 := State("q4"),
        q5 := State("q5"),
        q6 := State("q6"),
    },
    {"a", "b"},
    {
        s0: {epsilon: {q0, q6}},
        q0: {epsilon: {q1, q3}},
        q1: {
            "a": {q2},
        },
        q2: {
            epsilon: {q5},
        },
        q3: {
            "b": {q4},
        },
        q4: {
            epsilon: {q5},
        },
        q5: {
            epsilon: {q0, q6},
        },
    },
    {s0},
    {q6},
)
