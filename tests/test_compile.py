import pytest

import regular


# RegularExpression class compile tests


def test_regularexpression_compile_success():
    # should not raise exception
    regular.compile("[^01]")


def test_regularexpression_compile_fail():
    # should raise
    with pytest.raises(Exception):
        regular.compile("\\\\\\\\\\\\\\")
