from automata.dfa.samples import EVEN_NUMBER_OF_ZEROS
from automata.nfa import epsilon
from automata.nfa.nfa import NFA
from automata.nfa.samples import A_OR_B_WHOLE_STAR
from automata.regex.regex import RegExParser
from automata.state import State


def main():
    # sample DFAs
    print("1.", EVEN_NUMBER_OF_ZEROS.accepts("00100"))  # True
    print("2.", EVEN_NUMBER_OF_ZEROS.accepts("10"))  # False

    print()

    # sample NFAs
    print("3.", A_OR_B_WHOLE_STAR.accepts(""))  # True
    print("4.", A_OR_B_WHOLE_STAR.accepts("a"))  # True
    print("5.", A_OR_B_WHOLE_STAR.accepts("aabbbba"))  # True

    print()

    # manual re to NFA
    # "(a*)(b|c)"
    re = "a*b|c"
    tokens = RegExParser.tokenize(re)
    print("6a.", tokens)

    parsed_tokens = RegExParser.parse(tokens)
    print("6b.", parsed_tokens)

    compiled_token = RegExParser.compile(parsed_tokens)
    State.reset_naming()
    print("\n6c.")
    compiled_token.print_transition_function()

    print()

    # direct re to NFA
    re_to_nfa = RegExParser.to_nfa(re)
    State.reset_naming()
    print("7a.", re_to_nfa.initial)
    print("7b.", re_to_nfa.accepting)

    print()

    print("7c. Transition function of NFA from RE:")
    re_to_nfa.print_transition_function()

    print()

    # NFA to DFA

    print("8. cs/ece 374 5.1.2")

    print()

    cs_374_512_nfa = NFA(
        states={
            q0 := State("q0"),
            a_q1 := State("q1"),
            a_q2 := State("q2"),
            a_q3 := State("q3"),
        },
        alphabet={"0", "1"},
        transitions={
            q0: {epsilon: {a_q1}, "1": {a_q2}},
            a_q1: {"0": {a_q3}},
            a_q2: {epsilon: {a_q3}},
        },
        initial={q0},
        accepting={a_q3},
    )

    print("NFA states: ", cs_374_512_nfa.states)
    print("NFA initial states: ", cs_374_512_nfa.initial)
    print("NFA accepting states: ", cs_374_512_nfa.accepting)
    print()
    print("NFA transition function:")
    cs_374_512_nfa.print_transition_function()

    print()

    cs_374_512_dfa = cs_374_512_nfa.to_dfa()

    print("DFA states: ", cs_374_512_dfa.states)
    print("DFA initial states: ", cs_374_512_dfa.initial)
    print("DFA accepting state:", cs_374_512_dfa.accepting)
    print()
    print("DFA transition function:")
    cs_374_512_dfa.print_transition_function()

    print()

    print("9. hw03_3")

    hw03_3_nfa = NFA(
        {a_q1 := State("q1"), a_q2 := State("q2"), a_q3 := State("q3")},
        {"a", "b"},
        {
            a_q1: {"a": {a_q3}, epsilon: {a_q2}},
            a_q2: {"a": {a_q1}},
            a_q3: {"a": {a_q2}, "b": {a_q2, a_q3}},
        },
        {a_q1},
        {a_q2},
    )

    print()

    print("NFA states: ", hw03_3_nfa.states)
    print("NFA initial states: ", hw03_3_nfa.initial)
    print("NFA accepting states: ", hw03_3_nfa.accepting)
    print()
    print("NFA transition function:")
    hw03_3_nfa.print_transition_function()

    print()

    hw03_3_dfa = hw03_3_nfa.to_dfa()

    print("DFA states:", hw03_3_dfa.states)
    print("DFA initial state:", hw03_3_dfa.initial)
    print("DFA accepting states:", hw03_3_dfa.accepting)
    print()
    print("DFA transition function:")
    hw03_3_dfa.print_transition_function()

    print()

    print("10. nj_cs341")

    print()

    nj_cs341_p53_nfa = NFA(
        {
            b_q1 := State("q1"),
            b_q2 := State("q2"),
            b_q3 := State("q3"),
            b_q4 := State("q4"),
        },
        {"0", "1"},
        {
            b_q1: {"0": {b_q1}, "1": {b_q1, b_q2}},
            b_q2: {"0": {b_q3}, epsilon: {b_q3}},
            b_q3: {"1": {b_q4}},
            b_q4: {"0": {b_q4}, "1": {b_q4}},
        },
        {b_q1},
        {b_q4},
    )

    print("NFA states: ", nj_cs341_p53_nfa.states)
    print("NFA initial states: ", nj_cs341_p53_nfa.initial)
    print("NFA accepting states: ", nj_cs341_p53_nfa.accepting)
    print()
    print("NFA transition function:")
    nj_cs341_p53_nfa.print_transition_function()

    print()

    nj_cs341_p53_dfa = nj_cs341_p53_nfa.to_dfa()

    print("DFA states:", nj_cs341_p53_dfa.states)
    print("DFA initial state:", nj_cs341_p53_dfa.initial)
    print("DFA accepting states:", nj_cs341_p53_dfa.accepting)
    print()
    print("DFA transition function:")
    nj_cs341_p53_dfa.print_transition_function()


if __name__ == "__main__":
    main()
