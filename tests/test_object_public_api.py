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
    regex = regular.compile("[01]")
    regex2 = regular.compile("[34]")
    text = "10234510"
    m = regex.find(text)
    m2 = regex2.find(text)
    assert type(m) is regular.Match
    assert m.as_str() == "1"
    assert m2.as_str() == "3"


# Match range method


def test_match_range_method():
    regex = regular.compile("[01]")
    regex2 = regular.compile("[34]")
    text = "10234510"
    m = regex.find(text)
    m2 = regex2.find(text)
    assert type(m) is regular.Match
    assert type(m2) is regular.Match
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


# RegularExpression find_all tests


def test_regularexpression_find_all():
    regex = regular.compile("[01]")
    text = "0123410"
    i = regex.find_all(text)
    assert type(i) is list
    assert len(i) == 4
    for item in i:
        assert type(item) is regular.Match
    m1 = i[0]
    assert m1.start == 0 and m1.end == 1 and m1.text == "0"
    m2 = i[1]
    assert m2.start == 1 and m2.end == 2 and m2.text == "1"
    m3 = i[2]
    assert m3.start == 5 and m3.end == 6 and m3.text == "1"
    m4 = i[3]
    assert m4.start == 6 and m4.end == 7 and m4.text == "0"


def test_regularexpression_find_all_no_match():
    regex = regular.compile("[ab]")
    text = "0123410"
    i = regex.find_all(text)
    assert type(i) is list
    assert len(i) == 0


# RegularExpression find_iter tests


def test_regularexpression_find_iter():
    regex = regular.compile("[01]")
    text = "0123410"
    i = regex.find_iter(text)
    assert type(i) is regular.MatchesIterator
    # test iteration with next
    m1 = next(i)
    assert m1.start == 0 and m1.end == 1 and m1.text == "0"
    m2 = next(i)
    assert m2.start == 1 and m2.end == 2 and m2.text == "1"
    m3 = next(i)
    assert m3.start == 5 and m3.end == 6 and m3.text == "1"
    m4 = next(i)
    assert m4.start == 6 and m4.end == 7 and m4.text == "0"
    with pytest.raises(StopIteration):
        next(i)
    # test for loop
    i2 = regex.find_iter(text)
    for m in i2:
        assert type(m) is regular.Match
    # test cast to list collection
    i3 = regex.find_iter(text)
    col = list(i3)
    assert len(col) == 4
    for m in col:
        assert type(m) is regular.Match


def test_regularexpression_find_iter_no_match():
    regex = regular.compile("[ab]")
    text = "01234510"
    i = regex.find_iter(text)
    assert type(i) is regular.MatchesIterator
    # has empty/no match mechanics
    with pytest.raises(StopIteration):
        next(i)
    i2 = regex.find_iter(text)
    for m in i2:
        # does not raise exception when no matches
        pass
    i3 = regex.find_iter(text)
    # cast to list does not raise exception
    col = list(i3)
    assert len(col) == 0


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


# RegularExpression split tests


def test_regularexpression_split():
    regex = regular.compile(r"[ \t]+")
    text = "a b \t  c\td    e"
    m = regex.split(text)
    assert type(m) is list
    assert m == ["a", "b", "c", "d", "e"]


def test_regularexpression_split_no_match():
    regex = regular.compile(r"[01]+")
    text = "a b \t  c\td    e"
    m = regex.split(text)
    assert type(m) is list
    assert m == ["a b \t  c\td    e"]


# RegularExpression splitn tests


def test_regularexpression_splitn():
    regex = regular.compile(r"[ \t]+")
    text = "a b \t  c\td    e"
    m = regex.splitn(text, 2)
    assert type(m) is list
    assert m == ["a", "b \t  c\td    e"]
    m2 = regex.splitn(text, 3)
    assert type(m2) is list
    assert m2 == ["a", "b", "c\td    e"]
    m3 = regex.splitn(text, 0)
    assert m3 == []


def test_regularexpression_splitn_no_match():
    regex = regular.compile(r"[01]")
    text = "a b \t  c\td    e"
    m = regex.splitn(text, 3)
    assert type(m) is list
    assert m == ["a b \t  c\td    e"]


# RegularExpression split_iter tests


def test_regularexpression_split_iter():
    regex = regular.compile(r"[ \t]+")
    text = "a b \t  c\td    e"
    m = regex.split_iter(text)
    assert next(m) == "a"
    assert next(m) == "b"
    assert next(m) == "c"
    assert next(m) == "d"
    assert next(m) == "e"
    with pytest.raises(StopIteration):
        next(m)
    m2 = regex.split_iter(text)
    for match in m2:
        assert type(match) is str


def test_regularexpression_split_iter_no_match():
    regex = regular.compile(r"[01]")
    text = "a b \t  c\td    e"
    m = regex.split_iter(text)
    assert next(m) == "a b \t  c\td    e"
    with pytest.raises(StopIteration):
        next(m)
