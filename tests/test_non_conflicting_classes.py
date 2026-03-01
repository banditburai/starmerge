from starmerge import merge


def test_merges_non_conflicting_classes_correctly():
    assert merge("border-t border-white/10") == "border-t border-white/10"
    assert merge("border-t border-white") == "border-t border-white"
    assert merge("text-3.5xl text-black") == "text-3.5xl text-black"
