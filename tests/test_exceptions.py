import pytest

import regular


def test_regularexpression_compile_unclosed_charclass_exception():
    with pytest.raises(ValueError) as exc_info:
        # unclosed character class
        regular.compile("[0123")

    assert exc_info.type is ValueError
    assert "regex parse error" in exc_info.value.args[0]


def test_regularexpression_compile_exception_unclosed_charclass_raw_string():
    with pytest.raises(ValueError) as exc_info:
        # unclosed character class
        regular.compile(r"[0123")

    assert exc_info.type is ValueError
    assert "regex parse error" in exc_info.value.args[0]


def test_regularexpression_compile_exception_unrecognized_escape_raw_string():
    with pytest.raises(ValueError) as exc_info:
        # unnecessary escape in raw string
        # note that there is a Python side deprecation warning
        # if this is used outside of a raw string
        regular.compile(r"\/\d")

    assert exc_info.type is ValueError
    assert "regex parse error" in exc_info.value.args[0]
