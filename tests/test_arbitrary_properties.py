"""
Python equivalent of js-source/arbitrary-properties.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.
"""

import pytest
from tw_merge import tw_merge


def test_handles_arbitrary_property_conflicts_correctly():
    """Equivalent to the 'handles arbitrary property conflicts correctly' test in TypeScript."""
    assert tw_merge('[paint-order:markers] [paint-order:normal]') == '[paint-order:normal]'
    assert tw_merge('[paint-order:markers] [--my-var:2rem] [paint-order:normal] [--my-var:4px]') == '[paint-order:normal] [--my-var:4px]'


def test_handles_arbitrary_property_conflicts_with_modifiers_correctly():
    """Equivalent to the 'handles arbitrary property conflicts with modifiers correctly' test in TypeScript."""
    assert tw_merge('[paint-order:markers] hover:[paint-order:normal]') == '[paint-order:markers] hover:[paint-order:normal]'
    assert tw_merge('hover:[paint-order:markers] hover:[paint-order:normal]') == 'hover:[paint-order:normal]'
    assert tw_merge('hover:focus:[paint-order:markers] focus:hover:[paint-order:normal]') == 'focus:hover:[paint-order:normal]'
    assert tw_merge('[paint-order:markers] [paint-order:normal] [--my-var:2rem] lg:[--my-var:4px]') == '[paint-order:normal] [--my-var:2rem] lg:[--my-var:4px]'
    assert tw_merge('bg-[#B91C1C] bg-radial-[at_50%_75%] bg-radial-[at_25%_25%]') == 'bg-[#B91C1C] bg-radial-[at_25%_25%]'


def test_handles_complex_arbitrary_property_conflicts_correctly():
    """Equivalent to the 'handles complex arbitrary property conflicts correctly' test in TypeScript."""
    assert tw_merge('[-unknown-prop:::123:::] [-unknown-prop:url(https://hi.com)]') == '[-unknown-prop:url(https://hi.com)]'


def test_handles_important_modifier_correctly():
    """Equivalent to the 'handles important modifier correctly' test in TypeScript."""
    assert tw_merge('![some:prop] [some:other]') == '![some:prop] [some:other]'
    assert tw_merge('![some:prop] [some:other] [some:one] ![some:another]') == '[some:one] ![some:another]' 