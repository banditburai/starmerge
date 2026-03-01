from starmerge import merge


def test_merges_content_utilities_correctly():
    assert merge("content-['hello'] content-[attr(data-content)]") == 'content-[attr(data-content)]' 
