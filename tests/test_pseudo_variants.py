from starmerge import merge


def test_handles_pseudo_variants_conflicts_properly():
    assert merge('empty:p-2 empty:p-3') == 'empty:p-3'
    assert merge('hover:empty:p-2 hover:empty:p-3') == 'hover:empty:p-3'
    assert merge('read-only:p-2 read-only:p-3') == 'read-only:p-3'


def test_handles_pseudo_variant_group_conflicts_properly():
    assert merge('group-empty:p-2 group-empty:p-3') == 'group-empty:p-3'
    assert merge('peer-empty:p-2 peer-empty:p-3') == 'peer-empty:p-3'
    assert merge('group-empty:p-2 peer-empty:p-3') == 'group-empty:p-2 peer-empty:p-3'
    assert merge('hover:group-empty:p-2 hover:group-empty:p-3') == 'hover:group-empty:p-3'
    assert merge('group-read-only:p-2 group-read-only:p-3') == 'group-read-only:p-3' 
