from starmerge import tw_join


def test_strings():
    assert tw_join("") == ""
    assert tw_join("foo") == "foo"
    assert tw_join(True and "foo") == "foo"
    assert tw_join(False and "foo") == ""


def test_strings_variadic():
    assert tw_join("") == ""
    assert tw_join("foo", "bar") == "foo bar"
    assert tw_join(True and "foo", False and "bar", "baz") == "foo baz"
    assert tw_join(False and "foo", "bar", "baz", "") == "bar baz"


def test_arrays():
    assert tw_join([]) == ""
    assert tw_join(["foo"]) == "foo"
    assert tw_join(["foo", "bar"]) == "foo bar"
    assert tw_join(["foo", 0 and "bar", 1 and "baz"]) == "foo baz"


def test_arrays_nested():
    assert tw_join([[[]]]) == ""
    assert tw_join([[["foo"]]]) == "foo"
    assert tw_join([False, [["foo"]]]) == "foo"
    assert tw_join(["foo", ["bar", ["", [["baz"]]]]]) == "foo bar baz"


def test_arrays_variadic():
    assert tw_join([], []) == ""
    assert tw_join(["foo"], ["bar"]) == "foo bar"
    assert tw_join(["foo"], None, ["baz", ""], False, "", []) == "foo baz"
