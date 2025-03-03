"""
Python equivalent of js-source/pseudo-variants.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies that tw_merge correctly handles pseudo variants
and pseudo variant groups in Tailwind CSS classes.
"""

import pytest
from tw_merge import tw_merge


def test_handles_pseudo_variants_conflicts_properly():
    """Test if pseudo variants conflicts are handled properly."""
    assert tw_merge('empty:p-2 empty:p-3') == 'empty:p-3'
    assert tw_merge('hover:empty:p-2 hover:empty:p-3') == 'hover:empty:p-3'
    assert tw_merge('read-only:p-2 read-only:p-3') == 'read-only:p-3'


def test_handles_pseudo_variant_group_conflicts_properly():
    """Test if pseudo variant group conflicts are handled properly."""
    assert tw_merge('group-empty:p-2 group-empty:p-3') == 'group-empty:p-3'
    assert tw_merge('peer-empty:p-2 peer-empty:p-3') == 'peer-empty:p-3'
    assert tw_merge('group-empty:p-2 peer-empty:p-3') == 'group-empty:p-2 peer-empty:p-3'
    assert tw_merge('hover:group-empty:p-2 hover:group-empty:p-3') == 'hover:group-empty:p-3'
    assert tw_merge('group-read-only:p-2 group-read-only:p-3') == 'group-read-only:p-3' 