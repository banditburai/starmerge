"""
Python equivalent of js-source/tw-merge.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.
"""

import pytest
from tw_merge import tw_merge


def test_twmerge():
    """Test that tw_merge correctly handles various Tailwind CSS class merging scenarios."""
    assert tw_merge('mix-blend-normal mix-blend-multiply') == 'mix-blend-multiply'
    assert tw_merge('h-10 h-min') == 'h-min'
    assert tw_merge('stroke-black stroke-1') == 'stroke-black stroke-1'
    assert tw_merge('stroke-2 stroke-[3]') == 'stroke-[3]'
    assert tw_merge('outline-black outline-1') == 'outline-black outline-1'
    assert tw_merge('grayscale-0 grayscale-[50%]') == 'grayscale-[50%]'
    assert tw_merge('grow grow-[2]') == 'grow-[2]'
    assert tw_merge('grow', [None, False, [['grow-[2]']]]) == 'grow-[2]' 