"""
Python equivalent of js-source/default-config.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.
"""

import pytest
from tw_merge import get_default_config


def test_default_config_has_correct_types():
    """Equivalent to the 'default config has correct types' test in TypeScript."""
    default_config = get_default_config()
    
    # Check the cache size
    assert default_config['cache_size'] == 500
    
    # Check that non-existent properties are None/undefined
    assert default_config.get('nonExistent') is None
    
    # Check that class groups exist and have correct data
    assert default_config['class_groups']['display'][0] == 'block'
    
    # Check that class groups have expected nested structures
    overflow_group = default_config['class_groups']['overflow'][0]
    assert overflow_group['overflow'][0] == 'auto'
    
    # Check that non-existent properties in nested structures are None/undefined
    assert overflow_group.get('nonExistent') is None 