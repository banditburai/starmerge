"""
Python equivalent of js-source/non-tailwind-classes.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies that tw_merge preserves non-Tailwind classes while
still properly handling Tailwind classes.
"""

import pytest
from tw_merge import tw_merge


def test_does_not_alter_non_tailwind_classes():
    """Test if non-Tailwind classes are preserved while Tailwind classes are properly merged."""
    assert tw_merge('non-tailwind-class inline block') == 'non-tailwind-class block'
    assert tw_merge('inline block inline-1') == 'block inline-1'
    assert tw_merge('inline block i-inline') == 'block i-inline'
    assert tw_merge('focus:inline focus:block focus:inline-1') == 'focus:block focus:inline-1' 