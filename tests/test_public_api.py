"""
Python equivalent of js-source/public-api.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies that all public APIs of the library are properly exposed
and function as expected.
"""

import pytest
from tw_merge import (
    tw_merge,
    create_tailwind_merge,
    get_default_config,
    validators,
    merge_configs,
    extend_tailwind_merge,
    tw_join,
    from_theme,
)


def test_has_correct_export_types():
    """Test that all APIs are exported with the correct types."""
    assert callable(tw_merge)
    assert callable(create_tailwind_merge)
    assert callable(get_default_config)
    
    # Check validators object has all expected methods
    validator_methods = [
        "is_any",
        "is_arbitrary_image",
        "is_arbitrary_length",
        "is_arbitrary_number",
        "is_arbitrary_position",
        "is_arbitrary_shadow",
        "is_arbitrary_size",
        "is_arbitrary_value",
        "is_arbitrary_variable",
        "is_fraction",
        "is_integer",
        "is_length",
        "is_length_only",
        "is_never",
        "is_number",
        "is_percent",
        "is_shadow",
        "is_tshirt_size",
        "is_image",
    ]
    
    for method in validator_methods:
        assert callable(getattr(validators, method))
    
    assert len(validator_methods) == 19
    assert callable(merge_configs)
    assert callable(extend_tailwind_merge)
    assert callable(tw_join)


def test_twmerge_has_correct_inputs_and_outputs():
    """Test that tw_merge accepts the correct inputs and returns strings."""
    assert isinstance(tw_merge(''), str)
    assert isinstance(tw_merge('hello world'), str)
    assert isinstance(tw_merge('-:-:-:::---h-'), str)
    assert isinstance(tw_merge('hello world', '-:-:-:::---h-'), str)
    assert isinstance(tw_merge('hello world', '-:-:-:::---h-', '', 'something'), str)
    assert isinstance(tw_merge('hello world', None), str)
    assert isinstance(tw_merge('hello world', None, None), str)
    assert isinstance(tw_merge('hello world', None, None, False), str)
    assert isinstance(tw_merge('hello world', [None], [None, False]), str)
    assert isinstance(tw_merge('hello world', [None], [None, [False, 'some-class'], []]), str)


def test_createtailwindmerge_has_correct_inputs_and_outputs():
    """Test that create_tailwind_merge accepts the correct inputs and returns a function."""
    assert callable(create_tailwind_merge(get_default_config))
    assert callable(create_tailwind_merge(lambda: {
        "cache_size": 0,
        "theme": {},
        "class_groups": {},
        "conflicting_class_groups": {},
        "conflicting_class_group_modifiers": {},
        "order_sensitive_modifiers": [],
    }))

    tailwind_merge = create_tailwind_merge(lambda: {
        "cache_size": 20,
        "theme": {},
        "class_groups": {
            "fooKey": [{"fooKey": ["bar", "baz"]}],
            "fooKey2": [{"fooKey": ["qux", "quux"]}],
            "otherKey": ["nother", "group"],
        },
        "conflicting_class_groups": {
            "fooKey": ["otherKey"],
            "otherKey": ["fooKey", "fooKey2"],
        },
        "conflicting_class_group_modifiers": {},
        "order_sensitive_modifiers": [],
    })

    assert callable(tailwind_merge)
    assert isinstance(tailwind_merge(''), str)
    assert isinstance(tailwind_merge('hello world'), str)
    assert isinstance(tailwind_merge('-:-:-:::---h-'), str)
    assert isinstance(tailwind_merge('hello world', '-:-:-:::---h-'), str)
    assert isinstance(tailwind_merge('hello world', '-:-:-:::---h-', '', 'something'), str)
    assert isinstance(tailwind_merge('hello world', None), str)
    assert isinstance(tailwind_merge('hello world', None, None), str)
    assert isinstance(tailwind_merge('hello world', None, None, False), str)
    assert isinstance(tailwind_merge('hello world', [None], [None, False]), str)
    assert isinstance(tailwind_merge('hello world', [None], [None, [False, 'some-class'], []]), str)


def test_validators_have_correct_inputs_and_outputs():
    """Test that validators return boolean values."""
    assert isinstance(validators.is_fraction(''), bool)
    assert isinstance(validators.is_arbitrary_length(''), bool)
    assert isinstance(validators.is_integer(''), bool)
    assert isinstance(validators.is_arbitrary_value(''), bool)
    assert isinstance(validators.is_arbitrary_variable(''), bool)
    assert isinstance(validators.is_any(''), bool)
    assert isinstance(validators.is_tshirt_size(''), bool)
    assert isinstance(validators.is_arbitrary_size(''), bool)
    assert isinstance(validators.is_arbitrary_position(''), bool)
    assert isinstance(validators.is_arbitrary_image(''), bool)
    assert isinstance(validators.is_arbitrary_number(''), bool)
    assert isinstance(validators.is_arbitrary_shadow(''), bool)


def test_mergeconfigs_has_correct_inputs_and_outputs():
    """Test that merge_configs returns an object."""
    result = merge_configs(
        {
            "cache_size": 50,
            "theme": {},
            "class_groups": {
                "fooKey": [{"fooKey": ["one", "two"]}],
                "bla": [{"bli": ["blub", "blublub"]}],
            },
            "conflicting_class_groups": {},
            "conflicting_class_group_modifiers": {},
            "order_sensitive_modifiers": [],
        },
        {},
    )
    assert isinstance(result, dict)


def test_extendtailwindmerge_has_correct_inputs_and_outputs():
    """Test that extend_tailwind_merge returns a function."""
    assert callable(extend_tailwind_merge({}))


def test_fromtheme_has_correct_inputs_and_outputs():
    """Test that from_theme returns a function with expected properties."""
    assert callable(from_theme('spacing'))
    
    theme_getter = from_theme('foo')
    assert callable(theme_getter)
    assert getattr(theme_getter, 'is_theme_getter', False) is True
    assert theme_getter({"foo": ["hello"]}) == ["hello"]


def test_twjoin_has_correct_inputs_and_outputs():
    """Test that tw_join returns a string."""
    assert isinstance(tw_join(), str)
    assert isinstance(tw_join(''), str)
    assert isinstance(tw_join('', [False, None, None, 0, [], [False, [''], '']]), str) 