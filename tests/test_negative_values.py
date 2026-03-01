from starmerge import merge


def test_handles_negative_value_conflicts_correctly():
    assert merge('-m-2 -m-5') == '-m-5'
    assert merge('-top-12 -top-2000') == '-top-2000'


def test_handles_conflicts_between_positive_and_negative_values_correctly():
    assert merge('-m-2 m-auto') == 'm-auto'
    assert merge('top-12 -top-69') == '-top-69'


def test_handles_conflicts_across_groups_with_negative_values_correctly():
    assert merge('-right-1 inset-x-1') == 'inset-x-1'
    assert merge('hover:focus:-right-1 focus:hover:inset-x-1') == 'focus:hover:inset-x-1' 
