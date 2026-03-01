from starmerge import merge


def test_merges_classes_with_per_side_border_colors_correctly():
    assert merge('border-t-some-blue border-t-other-blue') == 'border-t-other-blue'
    assert merge('border-t-some-blue border-some-blue') == 'border-some-blue'
    assert merge('border-some-blue border-s-some-blue') == 'border-some-blue border-s-some-blue'
    assert merge('border-e-some-blue border-some-blue') == 'border-some-blue' 
