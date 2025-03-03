"""
Python equivalent of js-source/class-group-conflicts.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.
"""

import pytest
from tw_merge import tw_merge


def test_merges_classes_from_same_group_correctly():
    """Equivalent to the 'merges classes from same group correctly' test in TypeScript."""
    assert tw_merge('overflow-x-auto overflow-x-hidden') == 'overflow-x-hidden'
    assert tw_merge('basis-full basis-auto') == 'basis-auto'
    assert tw_merge('w-full w-fit') == 'w-fit'
    assert tw_merge('overflow-x-auto overflow-x-hidden overflow-x-scroll') == 'overflow-x-scroll'
    assert tw_merge('overflow-x-auto hover:overflow-x-hidden overflow-x-scroll') == 'hover:overflow-x-hidden overflow-x-scroll'
    assert tw_merge('overflow-x-auto hover:overflow-x-hidden hover:overflow-x-auto overflow-x-scroll') == 'hover:overflow-x-auto overflow-x-scroll'
    assert tw_merge('col-span-1 col-span-full') == 'col-span-full'
    assert tw_merge('gap-2 gap-px basis-px basis-3') == 'gap-px basis-3'


def test_merges_classes_from_font_variant_numeric_section_correctly():
    """Equivalent to the 'merges classes from Font Variant Numeric section correctly' test in TypeScript."""
    assert tw_merge('lining-nums tabular-nums diagonal-fractions') == 'lining-nums tabular-nums diagonal-fractions'
    assert tw_merge('normal-nums tabular-nums diagonal-fractions') == 'tabular-nums diagonal-fractions'
    assert tw_merge('tabular-nums diagonal-fractions normal-nums') == 'normal-nums'
    assert tw_merge('tabular-nums proportional-nums') == 'proportional-nums' 