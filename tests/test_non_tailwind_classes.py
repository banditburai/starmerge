from starmerge import merge


def test_does_not_alter_non_tailwind_classes():
    assert merge('non-tailwind-class inline block') == 'non-tailwind-class block'
    assert merge('inline block inline-1') == 'block inline-1'
    assert merge('inline block i-inline') == 'block i-inline'
    assert merge('focus:inline focus:block focus:inline-1') == 'focus:block focus:inline-1' 
