"""
Python equivalent of js-source/theme.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies the behavior of theme extension functionality in tailwind-merge.
"""

import pytest
from starmerge import merge, extend_tailwind_merge, from_theme


def test_theme_scale_can_be_extended():
    """Test that theme scale can be extended."""
    tailwind_merge = extend_tailwind_merge({
        'extend': {
            'theme': {
                'spacing': ['my-space'],
                'leading': ['my-leading'],
            },
        },
    })

    assert tailwind_merge('p-3 p-my-space p-my-margin') == 'p-my-space p-my-margin'
    assert tailwind_merge('leading-3 leading-my-space leading-my-leading') == 'leading-my-leading'


def test_theme_object_can_be_extended():
    """Test that theme object can be extended."""
    tailwind_merge = extend_tailwind_merge({
        'extend': {
            'theme': {
                'my-theme': ['hallo', 'hello'],
            },
            'classGroups': {
                'px': [{'px': [from_theme('my-theme')]}],
            },
        },
    })

    assert tailwind_merge('p-3 p-hello p-hallo') == 'p-3 p-hello p-hallo'
    assert tailwind_merge('px-3 px-hello px-hallo') == 'px-hallo' 