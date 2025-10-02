"""
Python equivalent of js-source/per-side-border-colors.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies that tw_merge correctly handles per-side border color classes,
including conflicts between specific sides and general border colors.
"""

import pytest
from starmerge import merge


def test_merges_classes_with_per_side_border_colors_correctly():
    """Test if per-side border color classes are merged correctly."""
    assert merge('border-t-some-blue border-t-other-blue') == 'border-t-other-blue'
    assert merge('border-t-some-blue border-some-blue') == 'border-some-blue'
    assert merge('border-some-blue border-s-some-blue') == 'border-some-blue border-s-some-blue'
    assert merge('border-e-some-blue border-some-blue') == 'border-some-blue' 