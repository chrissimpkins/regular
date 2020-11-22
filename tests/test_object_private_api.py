import pytest

import regular


def test_regularexpression_str_method():
    regex = regular.compile("[^01]")
    assert regex.__str__() == "RegularExpression with pattern:  [^01]"


def test_regularexpression_repr_method():
    regex = regular.compile("[^01]")
    assert regex.__repr__() == "RegularExpression with pattern:  [^01]"


def test_regularexpression_richcmp_eq_method():
    r1 = regular.compile("[^01]")
    r2 = regular.compile("[^01]")
    r3 = regular.compile("[10101]")
    assert r1 == r2
    assert (r1 == r3) is False
    assert r1 is not r2


def test_regularexpression_richcmp_ne_method():
    r1 = regular.compile("[10101]")
    r2 = regular.compile("[^01]")
    r3 = regular.compile("[10101]")
    assert r1 != r2
    assert (r1 != r3) is False
    assert r1 is not r2
