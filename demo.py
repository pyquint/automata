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
    e_to_a = NFA(
        states={
            q0 := State("q0"),
            q1 := State("q1"),
            q2 := State("q2"),
            q3 := State("q3"),
        },
        alphabet={"0", "1"},
        transitions={
            q0: {epsilon: {q1}, "1": {q2}},
            q1: {"0": {q3}},
            q2: {epsilon: {q3}},
        },
        initial={q0},
        accepting={q3},
    )

    print("8a. Sample NFA transition function:")
    e_to_a.print_transition_function()
    print()

    print("8b. Equivalent DFA's transition function:")
    dfa = e_to_a.to_dfa()
    dfa.print_transition_function()


if __name__ == "__main__":
    main()
