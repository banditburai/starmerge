from starmerge import merge


def test_merges_tailwind_classes_with_important_modifier_correctly():
    # Latest Tailwind CSS v3 syntax (! suffix)
    assert merge("font-medium! font-bold!") == "font-bold!"
    assert merge("font-medium! font-bold! font-thin") == "font-bold! font-thin"
    assert merge("right-2! -inset-x-px!") == "-inset-x-px!"
    assert merge("focus:inline! focus:block!") == "focus:block!"
    assert merge("[--my-var:20px]! [--my-var:30px]!") == "[--my-var:30px]!"

    # Tailwind CSS v3 legacy syntax
    assert merge("font-medium! !font-bold") == "!font-bold"

    assert merge("!font-medium !font-bold") == "!font-bold"
    assert merge("!font-medium !font-bold font-thin") == "!font-bold font-thin"
    assert merge("!right-2 !-inset-x-px") == "!-inset-x-px"
    assert merge("focus:!inline focus:!block") == "focus:!block"
    assert merge("![--my-var:20px] ![--my-var:30px]") == "![--my-var:30px]"
