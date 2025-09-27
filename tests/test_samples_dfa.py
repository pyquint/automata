from automata.dfa.samples import (
    EVEN_NUMBER_OF_ZEROS,
    EVEN_OCCURRENCE_EACH_CHAR,
    NO_MA_PLUS_X,
    NO_MAX,
)


def test_even_zeroes():
    assert EVEN_NUMBER_OF_ZEROS.accepts("00")
    assert EVEN_NUMBER_OF_ZEROS.accepts("001")
    assert EVEN_NUMBER_OF_ZEROS.accepts("1001")
    assert EVEN_NUMBER_OF_ZEROS.accepts("0000")
    assert EVEN_NUMBER_OF_ZEROS.accepts("10000")
    assert EVEN_NUMBER_OF_ZEROS.accepts("00001")
    assert EVEN_NUMBER_OF_ZEROS.accepts("100001")

    assert not EVEN_NUMBER_OF_ZEROS.accepts("")
    assert not EVEN_NUMBER_OF_ZEROS.accepts("a")
    assert not EVEN_NUMBER_OF_ZEROS.accepts("0a")
    assert not EVEN_NUMBER_OF_ZEROS.accepts("0")
    assert not EVEN_NUMBER_OF_ZEROS.accepts("01")
    assert not EVEN_NUMBER_OF_ZEROS.accepts("000")
    assert not EVEN_NUMBER_OF_ZEROS.accepts("0001")
    assert not EVEN_NUMBER_OF_ZEROS.accepts("10")
    assert not EVEN_NUMBER_OF_ZEROS.accepts("1000001")


def test_even_occurence_each_char():
    assert EVEN_OCCURRENCE_EACH_CHAR.accepts("aa")
    assert EVEN_OCCURRENCE_EACH_CHAR.accepts("bb")
    assert EVEN_OCCURRENCE_EACH_CHAR.accepts("cc")
    assert EVEN_OCCURRENCE_EACH_CHAR.accepts("abab")
    assert EVEN_OCCURRENCE_EACH_CHAR.accepts("bbacac")
    assert EVEN_OCCURRENCE_EACH_CHAR.accepts("acca")
    assert EVEN_OCCURRENCE_EACH_CHAR.accepts("aaaacbbacaacac")

    assert not EVEN_OCCURRENCE_EACH_CHAR.accepts("a")
    assert not EVEN_OCCURRENCE_EACH_CHAR.accepts("ab")
    assert not EVEN_OCCURRENCE_EACH_CHAR.accepts("abc")
    assert not EVEN_OCCURRENCE_EACH_CHAR.accepts("aab")
    assert not EVEN_OCCURRENCE_EACH_CHAR.accepts("aac")
    assert not EVEN_OCCURRENCE_EACH_CHAR.accepts("cabac")


def test_no_max():
    assert NO_MAX.accepts("a")
    assert NO_MAX.accepts("m")
    assert NO_MAX.accepts("x")
    assert NO_MAX.accepts("ma")
    assert NO_MAX.accepts("mx")
    assert NO_MAX.accepts("mamaaaa")
    assert NO_MAX.accepts("maaaaax")

    assert not NO_MAX.accepts("max")
    assert not NO_MAX.accepts("amax")
    assert not NO_MAX.accepts("amxmax")
    assert not NO_MAX.accepts("maxmax")
    assert not NO_MAX.accepts("xmxmaxmmaamx")


def test_no_ma_plus_x():
    assert NO_MA_PLUS_X.accepts("a")
    assert NO_MA_PLUS_X.accepts("m")
    assert NO_MA_PLUS_X.accepts("x")
    assert NO_MA_PLUS_X.accepts("ma")
    assert NO_MA_PLUS_X.accepts("mx")
    assert NO_MA_PLUS_X.accepts("mamaaaa")

    assert not NO_MA_PLUS_X.accepts("maaaaax")
    assert not NO_MA_PLUS_X.accepts("max")
    assert not NO_MA_PLUS_X.accepts("amax")
    assert not NO_MA_PLUS_X.accepts("amxmax")
    assert not NO_MA_PLUS_X.accepts("maxmax")
    assert not NO_MA_PLUS_X.accepts("xmxmaxmmaamx")
