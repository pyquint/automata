from automata.dfa.samples import EVEN_NUMBER_OF_ZEROS
from automata.nfa.samples import A_OR_B_WHOLE_STAR


def main():
    print("1.", EVEN_NUMBER_OF_ZEROS.accepts("00100"))  # True
    print("2.", EVEN_NUMBER_OF_ZEROS.accepts("10"))  # False

    print()

    print("3. ", A_OR_B_WHOLE_STAR.accepts(""))  # True
    print("4. ", A_OR_B_WHOLE_STAR.accepts("a"))  # True
    print("5. ", A_OR_B_WHOLE_STAR.accepts("aabbbba"))  # True


if __name__ == "__main__":
    main()
