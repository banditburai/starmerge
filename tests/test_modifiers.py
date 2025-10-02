"""
Python equivalent of js-source/modifiers.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies the handling of modifiers (both prefix and postfix) in tw_merge.
"""

import pytest
from starmerge import merge, create_tailwind_merge


def test_conflicts_across_prefix_modifiers():
    """Test handling of conflicts across prefix modifiers like hover: and focus:."""
    assert merge('hover:block hover:inline') == 'hover:inline'
    assert merge('hover:block hover:focus:inline') == 'hover:block hover:focus:inline'
    assert merge('hover:block hover:focus:inline focus:hover:inline') == 'hover:block focus:hover:inline'
    assert merge('focus-within:inline focus-within:block') == 'focus-within:block'


def test_conflicts_across_postfix_modifiers():
    """Test handling of conflicts across postfix modifiers like /7, /8 and fractions."""
    assert merge('text-lg/7 text-lg/8') == 'text-lg/8'
    assert merge('text-lg/none leading-9') == 'text-lg/none leading-9'
    assert merge('leading-9 text-lg/none') == 'text-lg/none'
    assert merge('w-full w-1/2') == 'w-1/2'

    # Test with custom configuration
    custom_tw_merge = create_tailwind_merge(lambda: {
        "cache_size": 10,
        "theme": {},
        "class_groups": {
            "foo": ["foo-1/2", "foo-2/3"],
            "bar": ["bar-1", "bar-2"],
            "baz": ["baz-1", "baz-2"],
        },
        "conflicting_class_groups": {},
        "conflicting_class_group_modifiers": {
            "baz": ["bar"],
        },
        "order_sensitive_modifiers": [],
    })

    assert custom_tw_merge('foo-1/2 foo-2/3') == 'foo-2/3'
    assert custom_tw_merge('bar-1 bar-2') == 'bar-2'
    assert custom_tw_merge('bar-1 baz-1') == 'bar-1 baz-1'
    assert custom_tw_merge('bar-1/2 bar-2') == 'bar-2'
    assert custom_tw_merge('bar-2 bar-1/2') == 'bar-1/2'
    assert custom_tw_merge('bar-1 baz-1/2') == 'baz-1/2'


def test_sorts_modifiers_correctly():
    """Test that modifiers are sorted correctly when determining conflicts."""
    assert merge('c:d:e:block d:c:e:inline') == 'd:c:e:inline'
    assert merge('*:before:block *:before:inline') == '*:before:inline'
    assert merge('*:before:block before:*:inline') == '*:before:block before:*:inline'
    assert merge('x:y:*:z:block y:x:*:z:inline') == 'y:x:*:z:inline'


def test_sorts_modifiers_correctly_according_to_ordersensitivemodifiers():
    """Test that order-sensitive modifiers are respected when determining conflicts."""
    custom_tw_merge = create_tailwind_merge(lambda: {
        "cache_size": 10,
        "theme": {},
        "class_groups": {
            "foo": ["foo-1", "foo-2"],
        },
        "conflicting_class_groups": {},
        "conflicting_class_group_modifiers": {},
        "order_sensitive_modifiers": ["a", "b"],
    })

    assert custom_tw_merge('c:d:e:foo-1 d:c:e:foo-2') == 'd:c:e:foo-2'
    assert custom_tw_merge('a:b:foo-1 a:b:foo-2') == 'a:b:foo-2'
    assert custom_tw_merge('a:b:foo-1 b:a:foo-2') == 'a:b:foo-1 b:a:foo-2'
    assert custom_tw_merge('x:y:a:z:foo-1 y:x:a:z:foo-2') == 'y:x:a:z:foo-2' 