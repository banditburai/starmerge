"""
Python equivalent of js-source/negative-values.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies the handling of negative value classes in tw_merge,
including conflicts between negative values and between positive and negative values.
"""

import pytest
from tw_merge import tw_merge


def test_handles_negative_value_conflicts_correctly():
    """Test if negative value conflicts are handled correctly."""
    assert tw_merge('-m-2 -m-5') == '-m-5'
    assert tw_merge('-top-12 -top-2000') == '-top-2000'


def test_handles_conflicts_between_positive_and_negative_values_correctly():
    """Test if conflicts between positive and negative values are handled correctly."""
    assert tw_merge('-m-2 m-auto') == 'm-auto'
    assert tw_merge('top-12 -top-69') == '-top-69'


def test_handles_conflicts_across_groups_with_negative_values_correctly():
    """Test if conflicts across groups with negative values are handled correctly."""
    assert tw_merge('-right-1 inset-x-1') == 'inset-x-1'
    assert tw_merge('hover:focus:-right-1 focus:hover:inset-x-1') == 'focus:hover:inset-x-1' 