import pytest

from automata import State
from automata.nfa import epsilon
from automata.nfa.nfa import NFA
from automata.nfa.samples import A_OR_B_WHOLE_STAR
from automata.regex import RegExParser
from automata.regex.regex import ParsingError


def test_tokenize_unrecognized_character():
    for c in "!@#$%^&-= ,./<>?;':\"[]{}\\`~ ":
        with pytest.raises(ParsingError):
            _ = RegExParser.tokenize(f"ab{c}")


def test_valid_regex():
    _ = RegExParser.to_nfa("a|b")
    _ = RegExParser.to_nfa("a|b|c")
    _ = RegExParser.to_nfa("a*b")
    _ = RegExParser.to_nfa("(ab)*|c*")
    _ = RegExParser.to_nfa("aaaaa")
    _ = RegExParser.to_nfa("a|b|c|d")
    _ = RegExParser.to_nfa("(a|b|c|d)|(z*)")
    _ = RegExParser.to_nfa("((a|b|c|d)|((z*)|a))*")
    _ = RegExParser.to_nfa("((((a)))*)")


def test_to_nfa_invalid_union():
    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("|")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("a|")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("a||")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("|b")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("||b")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("a||b")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("a|||b")


def test_to_nfa_invalid_star():
    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("*")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("*a")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("**a")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("a**")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("a**b")


def test_to_nfa_invalid_plus():
    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("+")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("+a")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("++a")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("a++")

    with pytest.raises(ParsingError):
        _ = RegExParser.to_nfa("a++b")


def test_re_nfa_equality():
    ab = NFA(
        {q0 := State(), q1 := State(), q2 := State(), q3 := State()},
        {"a", "b"},
        {q0: {"a": {q1}}, q1: {epsilon: {q2}}, q2: {"b": {q3}}},
        {q0},
        {q3},
    )

    State.reset_naming()

    ab_from_re: NFA = RegExParser.to_nfa("ab")

    assert ab.states == ab_from_re.states
    assert ab.alphabet == ab_from_re.alphabet
    assert ab.initial == ab_from_re.initial
    assert ab.accepting == ab_from_re.accepting
    assert ab.transitions == ab_from_re.transitions

    a_or_b_whole_star_from_re = RegExParser.to_nfa("(a|b)*")

    assert A_OR_B_WHOLE_STAR.accepts("")
    assert A_OR_B_WHOLE_STAR.accepts("a")
    assert A_OR_B_WHOLE_STAR.accepts("b")
    assert A_OR_B_WHOLE_STAR.accepts("ab")
    assert A_OR_B_WHOLE_STAR.accepts("aba")
    assert A_OR_B_WHOLE_STAR.accepts("baaabbbbabababb")

    assert a_or_b_whole_star_from_re.accepts("")
    assert a_or_b_whole_star_from_re.accepts("a")
    assert a_or_b_whole_star_from_re.accepts("b")
    assert a_or_b_whole_star_from_re.accepts("ab")
    assert a_or_b_whole_star_from_re.accepts("aba")
    assert a_or_b_whole_star_from_re.accepts("baaabbbbabababb")
