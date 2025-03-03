"""
Python equivalent of js-source/content-utilities.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.
"""

import pytest
from tw_merge import tw_merge


def test_merges_content_utilities_correctly():
    """Equivalent to the 'merges content utilities correctly' test in TypeScript."""
    assert tw_merge("content-['hello'] content-[attr(data-content)]") == 'content-[attr(data-content)]' 