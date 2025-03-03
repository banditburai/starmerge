"""
Python equivalent of js-source/standalone-classes.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies the behavior of the tw_merge function with standalone classes.
"""

import pytest
from tw_merge import tw_merge


def test_merges_standalone_classes_from_same_group_correctly():
    """Test that standalone classes from the same group are merged correctly."""
    assert tw_merge('inline block') == 'block'
    assert tw_merge('hover:block hover:inline') == 'hover:inline'
    assert tw_merge('hover:block hover:block') == 'hover:block'
    assert tw_merge('inline hover:inline focus:inline hover:block hover:focus:block') == \
        'inline focus:inline hover:block hover:focus:block'
    assert tw_merge('underline line-through') == 'line-through'
    assert tw_merge('line-through no-underline') == 'no-underline' 