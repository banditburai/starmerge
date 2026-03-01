from starmerge import merge


def test_merges_standalone_classes_from_same_group_correctly():
    assert merge('inline block') == 'block'
    assert merge('hover:block hover:inline') == 'hover:inline'
    assert merge('hover:block hover:block') == 'hover:block'
    assert merge('inline hover:inline focus:inline hover:block hover:focus:block') == \
        'inline focus:inline hover:block hover:focus:block'
    assert merge('underline line-through') == 'line-through'
    assert merge('line-through no-underline') == 'no-underline' 
