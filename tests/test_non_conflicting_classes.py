"""
Python equivalent of js-source/non-conflicting-classes.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies that tw_merge properly handles non-conflicting classes
by preserving them in the output.
"""

import pytest
from starmerge import merge


def test_merges_non_conflicting_classes_correctly():
    """Test if non-conflicting classes are merged correctly and preserved."""
    assert merge('border-t border-white/10') == 'border-t border-white/10'
    assert merge('border-t border-white') == 'border-t border-white'
    assert merge('text-3.5xl text-black') == 'text-3.5xl text-black' 