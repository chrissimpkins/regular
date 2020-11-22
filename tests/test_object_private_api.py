import pytest

import regular


def test_regularexpression_str_method():
    regex = regular.compile("[^01]")
    assert regex.__str__() == "RegularExpression with pattern:  [^01]"


def test_regularexpression_repr_method():
    regex = regular.compile("[^01]")
    assert regex.__repr__() == "RegularExpression with pattern:  [^01]"
