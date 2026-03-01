from starmerge import extend_tailwind_merge


def test_prefix_working_correctly():
    tw_merge = extend_tailwind_merge({
        "prefix": "tw"
    })
    assert tw_merge('tw:block tw:hidden') == 'tw:hidden'
    assert tw_merge('block hidden') == 'block hidden'

    assert tw_merge('tw:p-3 tw:p-2') == 'tw:p-2'
    assert tw_merge('p-3 p-2') == 'p-3 p-2'

    assert tw_merge('tw:right-0! tw:inset-0!') == 'tw:inset-0!'

    assert tw_merge('tw:hover:focus:right-0! tw:focus:hover:inset-0!') == 'tw:focus:hover:inset-0!' 
