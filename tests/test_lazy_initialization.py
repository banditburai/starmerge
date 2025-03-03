"""
Python equivalent of js-source/lazy-initialization.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies the lazy initialization behavior of the createTailwindMerge function.
"""

import pytest
from unittest.mock import Mock

from tw_merge import create_tailwind_merge
from tw_merge.lib.default_config import get_default_config


def test_lazy_initialization():
    """Test that createTailwindMerge performs lazy initialization."""
    # Create a mock function that wraps get_default_config
    init_mock = Mock(side_effect=get_default_config)
    
    # Create the tailwind_merge function with our mock
    tailwind_merge = create_tailwind_merge(init_mock)
    
    # Verify the init function wasn't called during creation
    assert init_mock.call_count == 0
    
    # First call to tailwind_merge should trigger initialization
    tailwind_merge()
    
    # Verify the init function was called exactly once
    assert init_mock.call_count == 1
    
    # Subsequent calls should not trigger initialization again
    tailwind_merge()
    tailwind_merge('')
    tailwind_merge('px-2 p-3 p-4')
    
    # Verify the init function was still only called once
    assert init_mock.call_count == 1 