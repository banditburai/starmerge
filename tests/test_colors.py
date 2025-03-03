"""
Python equivalent of js-source/colors.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.
"""

import pytest
from tw_merge import tw_merge


def test_handles_color_conflicts_properly():
    """Equivalent to the 'handles color conflicts properly' test in TypeScript."""
    assert tw_merge('bg-grey-5 bg-hotpink') == 'bg-hotpink'
    assert tw_merge('hover:bg-grey-5 hover:bg-hotpink') == 'hover:bg-hotpink'
    assert tw_merge('stroke-[hsl(350_80%_0%)] stroke-[10px]') == 'stroke-[hsl(350_80%_0%)] stroke-[10px]' 