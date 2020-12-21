import pytest

import regular
from regular import Match, RegularExpression

# Match class


def test_match_str_method():
    regex = regular.compile("[01]")
    text = "10234510"
    m = regex.find(text)
    assert type(m) is Match
    assert m.__str__() == 'Match < start: 0, end: 1, text: "1" >'


def test_match_repr_method():
    regex = regular.compile("[01]")
    text = "10234510"
    m = regex.find(text)
    assert type(m) is Match
    assert m.__repr__() == 'Match < start: 0, end: 1, text: "1" >'


def test_match_richcmp_eq_method():
    r1 = regular.compile("[01]")
    r2 = regular.compile("[34]")
    r3 = regular.compile("[01]")
    text = "01234501"
    text2 = "23450101"
    m1 = r1.find(text)
    m2 = r2.find(text)
    m3 = r3.find(text)
    m4 = r1.find(text2)  # same match string, different location
    assert type(m1) is Match
    assert type(m2) is Match
    assert type(m3) is Match
    assert type(m4) is Match
    assert m1 == m3
    assert (m1 == m2) is False
    assert m4.text == m1.text
    assert (m1 == m4) is False  # matched same string, but different location


def test_match_richcmp_ne_method():
    r1 = regular.compile("[01]")
    r2 = regular.compile("[34]")
    r3 = regular.compile("[01]")
    text = "01234501"
    text2 = "23450101"
    m1 = r1.find(text)
    m2 = r2.find(text)
    m3 = r3.find(text)
    m4 = r1.find(text2)  # same match string, different location
    assert type(m1) is Match
    assert type(m2) is Match
    assert type(m3) is Match
    assert type(m4) is Match
    assert (m1 != m3) is False
    assert m1 != m2
    assert m4.text == m1.text
    assert m1 != m4  # matched same string, but different location


# RegularExpression class


def test_regularexpression_str_method():
    regex = regular.compile("[^01]")
    assert type(regex) is RegularExpression
    assert regex.__str__() == "RegularExpression with pattern:  [^01]"


def test_regularexpression_repr_method():
    regex = regular.compile("[^01]")
    assert type(regex) is RegularExpression
    assert regex.__repr__() == "RegularExpression with pattern:  [^01]"


def test_regularexpression_richcmp_eq_method():
    r1 = regular.compile("[^01]")
    r2 = regular.compile("[^01]")
    r3 = regular.compile("[10101]")
    assert type(r1) is RegularExpression
    assert type(r2) is RegularExpression
    assert type(r3) is RegularExpression
    assert r1 == r2  # assert equality
    assert r1 is not r2  # but they are not the same object
    assert (r1 == r3) is False


def test_regularexpression_richcmp_ne_method():
    r1 = regular.compile("[10101]")
    r2 = regular.compile("[^01]")
    r3 = regular.compile("[10101]")
    assert type(r1) is RegularExpression
    assert type(r2) is RegularExpression
    assert type(r3) is RegularExpression
    assert r1 != r2
    assert (r1 != r3) is False
    assert r1 is not r2
