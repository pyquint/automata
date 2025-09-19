from automata import DFA, State

EVEN_NUMBER_OF_ZEROS = DFA(
    states={q_0 := State("q0"), q_1 := State("q1")},
    alphabet={"0", "1"},
    transitions={q_0: {"0": q_1, "1": q_0}, q_1: {"0": q_0, "1": q_1}},
    initial=q_0,
    accepting={q_0},
)

# ^(?:[abc]{2})*$
EVEN_OCCURRENCE_EACH_CHAR = DFA(
    states={
        q_0 := State("q_0"),
        q_1 := State("q_1"),
        q_2 := State("q_2"),
        q_3 := State("q_3"),
        q_4 := State("q_4"),
        q_5 := State("q_5"),
        q_6 := State("q_6"),
        q_7 := State("q_7"),
    },
    alphabet={"a", "b", "c"},
    transitions={
        q_0: {"a": q_1, "b": q_2, "c": q_4},
        q_1: {"a": q_0, "b": q_3, "c": q_5},
        q_2: {"a": q_3, "b": q_0, "c": q_6},
        q_3: {"a": q_2, "b": q_1, "c": q_7},
        q_4: {"a": q_5, "b": q_6, "c": q_0},
        q_5: {"a": q_4, "b": q_7, "c": q_1},
        q_6: {"a": q_7, "b": q_4, "c": q_2},
        q_7: {"a": q_6, "b": q_5, "c": q_3},
    },
    initial=q_0,
    accepting={q_0},
)

# ^(?![ax]*max)[amx]*$
NO_MAX = DFA(
    states={
        q_0 := State("q_0"),
        q_1 := State("q_1"),
        q_2 := State("q_2"),
        q_3 := State("q_3"),
    },
    alphabet={"a", "m", "x"},
    transitions={
        q_0: {"a": q_0, "m": q_1, "x": q_0},
        q_1: {"a": q_2, "m": q_1, "x": q_0},
        q_2: {"a": q_0, "m": q_1, "x": q_3},
        q_3: {"a": q_3, "m": q_3, "x": q_3},
    },
    initial=q_0,
    accepting={q_0, q_1, q_2},
)

# ^(?![ax]*max)[amx]*$
NO_MA_PLUS_X = DFA(
    states={
        q_0 := State("q_0"),
        q_1 := State("q_1"),
        q_2 := State("q_2"),
        q_3 := State("q_3"),
    },
    alphabet={"a", "m", "x"},
    transitions={
        q_0: {"a": q_0, "m": q_1, "x": q_0},
        q_1: {"a": q_2, "m": q_1, "x": q_0},
        q_2: {"a": q_2, "m": q_1, "x": q_3},
        q_3: {"a": q_3, "m": q_3, "x": q_3},
    },
    initial=q_0,
    accepting={q_0, q_1, q_2},
)
