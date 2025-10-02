"""
Python equivalent of js-source/standalone-classes.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies the behavior of the tw_merge function with standalone classes.
"""

import pytest
from starmerge import merge


def test_merges_standalone_classes_from_same_group_correctly():
    """Test that standalone classes from the same group are merged correctly."""
    assert merge('inline block') == 'block'
    assert merge('hover:block hover:inline') == 'hover:inline'
    assert merge('hover:block hover:block') == 'hover:block'
    assert merge('inline hover:inline focus:inline hover:block hover:focus:block') == \
        'inline focus:inline hover:block hover:focus:block'
    assert merge('underline line-through') == 'line-through'
    assert merge('line-through no-underline') == 'no-underline' 