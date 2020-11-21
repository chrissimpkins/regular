import pytest

import regular

# RegularExpression auxiliary method tests


def test_regularexpression_as_str():
    re = regular.compile("[^01]")
    assert re.as_str() == "[^01]"


# match tests


def test_regularexpression_is_match():
    re = regular.compile("[01]{3}")
    test_string = "This string includes 010"
    assert re.is_match(test_string)


def test_regularexpression_is_match_false():
    re = regular.compile("[01]{3}")
    test_string = "This string includes 0"
    assert re.is_match(test_string) is False
