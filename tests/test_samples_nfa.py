from automata import State
from automata.nfa.samples import A_OR_B_WHOLE_STAR


def test_a_or_b_whole_star():
    assert A_OR_B_WHOLE_STAR.accepts("")
    assert A_OR_B_WHOLE_STAR.accepts("a")
    assert A_OR_B_WHOLE_STAR.accepts("b")
    assert A_OR_B_WHOLE_STAR.accepts("ab")
    assert A_OR_B_WHOLE_STAR.accepts("aba")
    assert A_OR_B_WHOLE_STAR.accepts("baaabbbbabababb")

    assert not A_OR_B_WHOLE_STAR.accepts("c")
    assert not A_OR_B_WHOLE_STAR.accepts("abc")

    # the e-closure of a state includes itself
    assert A_OR_B_WHOLE_STAR.epsilon_closure({State("s0")}) == {
        State("s0"),
        State("q0"),
        State("q1"),
        State("q3"),
        State("q6"),
    }

    assert A_OR_B_WHOLE_STAR.epsilon_closure({State("q5")}) == {
        State("q0"),
        State("q1"),
        State("q3"),
        State("q5"),
        State("q6"),
    }
