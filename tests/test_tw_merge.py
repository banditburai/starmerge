"""
Python equivalent of js-source/tw-merge.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.
"""

import pytest
from starmerge import merge


def test_merge():
    """Test that merge correctly handles various Tailwind CSS class merging scenarios."""
    assert merge('mix-blend-normal mix-blend-multiply') == 'mix-blend-multiply'
    assert merge('h-10 h-min') == 'h-min'
    assert merge('stroke-black stroke-1') == 'stroke-black stroke-1'
    assert merge('stroke-2 stroke-[3]') == 'stroke-[3]'
    assert merge('outline-black outline-1') == 'outline-black outline-1'
    assert merge('grayscale-0 grayscale-[50%]') == 'grayscale-[50%]'
    assert merge('grow grow-[2]') == 'grow-[2]'
    assert merge('grow', [None, False, [['grow-[2]']]]) == 'grow-[2]' 