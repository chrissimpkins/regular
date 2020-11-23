import pytest

import regular

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Match class tests
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Match class import


def test_match_obj_import():
    from regular import Match


# Match as_str method


def test_match_as_str_method():
    from regular import Match

    regex = regular.compile("[01]")
    regex2 = regular.compile("[34]")
    text = "10234510"
    m = regex.find(text)
    m2 = regex2.find(text)
    assert type(m) is Match
    assert m.as_str() == "1"
    assert m2.as_str() == "3"


# Match range method


def test_match_range_method():
    from regular import Match

    regex = regular.compile("[01]")
    regex2 = regular.compile("[34]")
    text = "10234510"
    m = regex.find(text)
    m2 = regex2.find(text)
    assert type(m) is Match
    assert type(m2) is Match
    assert m.range() == (0, 1)
    assert m2.range() == (3, 4)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# RegularExpression class tests
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# RegularExpression class import


def test_regularexpression_obj_import():
    from regular import RegularExpression


# RegularExpression auxiliary method tests


def test_regularexpression_as_str():
    regex = regular.compile("[^01]")
    assert regex.as_str() == "[^01]"


# RegularExpression find tests


def test_regularexpression_find():
    regex = regular.compile(r"\b\w{13}\b")
    test_string = "I categorically deny having triskaidekaphobia."
    m = regex.find(test_string)
    assert m.start == 2
    assert m.end == 15
    assert m.range() == (2, 15)
    assert m.text == "categorically"
    assert test_string[m.start : m.end] == "categorically"


def test_regularexpression_find_no_match():
    regex = regular.compile("[01]")
    test_string = "I categorically deny having triskaidekaphobia."
    m = regex.find(test_string)
    assert m is None


# RegularExpression match tests


def test_regularexpression_is_match():
    regex = regular.compile("[01]{3}")
    test_string = "This string includes 010"
    assert regex.is_match(test_string)


def test_regularexpression_is_match_false():
    regex = regular.compile("[01]{3}")
    test_string = "This string includes 0"
    assert regex.is_match(test_string) is False


# RegularExpression replace tests


def test_regularexpression_replace():
    regex = regular.compile("[^01]+")
    assert regex.replace("1078910", "") == "1010"


def test_regularexpression_replace_n_1():
    # performs a single replacement
    regex = regular.compile("[01]")
    assert regex.replace("1078910", "") == "078910"


def test_regularexpression_replace_capture_groups():
    regex = regular.compile(r"(?P<last>[^,\s]+),\s+(?P<first>\S+)")
    assert regex.replace("Springsteen, Bruce", "$first $last") == "Bruce Springsteen"


def test_regularexpression_replace_capture_groups_escapes():
    regex = regular.compile(r"(?P<first>\w+)\s+(?P<second>\w+)")
    assert regex.replace("deep fried", "${first}_$second") == "deep_fried"


def test_regularexpression_replace_no_match():
    regex = regular.compile(r"\d")
    assert regex.replace("abcdefg", "") == "abcdefg"


def test_regularexpression_replace_all():
    regex = regular.compile("[01]")
    assert regex.replace_all("1078910", "") == "789"


def test_regularexpression_replace_all_no_match():
    regex = regular.compile(r"[a-z]")
    assert regex.replace_all("1078910", "") == "1078910"


def test_regularexpression_replacen():
    regex = regular.compile("[01]")
    assert regex.replacen("1078910", 2, "") == "78910"


def test_regularexpression_replacen_no_match():
    regex = regular.compile("[a-z]")
    assert regex.replacen("1078910", 2, "") == "1078910"
