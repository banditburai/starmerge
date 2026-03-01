from starmerge import merge


def test_merges_classes_from_same_group_correctly():
    assert merge("overflow-x-auto overflow-x-hidden") == "overflow-x-hidden"
    assert merge("basis-full basis-auto") == "basis-auto"
    assert merge("w-full w-fit") == "w-fit"
    assert (
        merge("overflow-x-auto overflow-x-hidden overflow-x-scroll")
        == "overflow-x-scroll"
    )
    assert (
        merge("overflow-x-auto hover:overflow-x-hidden overflow-x-scroll")
        == "hover:overflow-x-hidden overflow-x-scroll"
    )
    assert (
        merge(
            "overflow-x-auto hover:overflow-x-hidden hover:overflow-x-auto overflow-x-scroll"
        )
        == "hover:overflow-x-auto overflow-x-scroll"
    )
    assert merge("col-span-1 col-span-full") == "col-span-full"
    assert merge("gap-2 gap-px basis-px basis-3") == "gap-px basis-3"


def test_merges_classes_from_font_variant_numeric_section_correctly():
    assert (
        merge("lining-nums tabular-nums diagonal-fractions")
        == "lining-nums tabular-nums diagonal-fractions"
    )
    assert (
        merge("normal-nums tabular-nums diagonal-fractions")
        == "tabular-nums diagonal-fractions"
    )
    assert merge("tabular-nums diagonal-fractions normal-nums") == "normal-nums"
    assert merge("tabular-nums proportional-nums") == "proportional-nums"
