"""
Python equivalent of js-source/merge-configs.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies the merge_configs function behaves correctly when merging configurations.
"""

import pytest
from tw_merge.lib.merge_configs import merge_configs


def test_mergeconfigs_has_correct_behavior():
    """Test that mergeConfigs correctly merges configuration objects."""
    result = merge_configs(
        {
            "cache_size": 50,
            "prefix": "tw",
            "theme": {
                "hi": ["ho"],
                "themeToOverride": ["to-override"],
            },
            "class_groups": {
                "fooKey": [{"fooKey": ["one", "two"]}],
                "bla": [{"bli": ["blub", "blublub"]}],
                "groupToOverride": ["this", "will", "be", "overridden"],
                "groupToOverride2": ["this", "will", "not", "be", "overridden"],
            },
            "conflicting_class_groups": {
                "toOverride": ["groupToOverride"],
            },
            "conflicting_class_group_modifiers": {
                "hello": ["world"],
                "toOverride": ["groupToOverride-2"],
            },
            "order_sensitive_modifiers": ["order-1"],
        },
        {
            "prefix": None,
            "override": {
                "theme": {
                    "themeToOverride": ["overridden"],
                },
                "class_groups": {
                    "groupToOverride": ["I", "overrode", "you"],
                    "groupToOverride2": None,
                },
                "conflicting_class_groups": {
                    "toOverride": ["groupOverridden"],
                },
                "conflicting_class_group_modifiers": {
                    "toOverride": ["overridden-2"],
                },
                "order_sensitive_modifiers": ["order-2"],
            },
            "extend": {
                "class_groups": {
                    "fooKey": [{"fooKey": ["bar", "baz"]}],
                    "fooKey2": [{"fooKey": ["qux", "quux"]}],
                    "otherKey": ["nother", "group"],
                    "groupToOverride": ["extended"],
                },
                "conflicting_class_groups": {
                    "fooKey": ["otherKey"],
                    "otherKey": ["fooKey", "fooKey2"],
                },
                "conflicting_class_group_modifiers": {
                    "hello": ["world2"],
                },
                "order_sensitive_modifiers": ["order-3"],
            },
        },
    )

    # Check the merged config has the expected structure and values
    assert result["cache_size"] == 50
    assert result["prefix"] == "tw"
    
    # Check theme
    assert result["theme"]["hi"] == ["ho"]
    assert result["theme"]["themeToOverride"] == ["overridden"]
    
    # Check class_groups
    assert result["class_groups"]["fooKey"] == [{"fooKey": ["one", "two"]}, {"fooKey": ["bar", "baz"]}]
    assert result["class_groups"]["bla"] == [{"bli": ["blub", "blublub"]}]
    assert result["class_groups"]["fooKey2"] == [{"fooKey": ["qux", "quux"]}]
    assert result["class_groups"]["otherKey"] == ["nother", "group"]
    assert result["class_groups"]["groupToOverride"] == ["I", "overrode", "you", "extended"]
    
    # Match TypeScript behavior: groupToOverride2 should be preserved even when None is passed
    assert "groupToOverride2" in result["class_groups"]
    assert result["class_groups"]["groupToOverride2"] == ["this", "will", "not", "be", "overridden"]
    
    # Check conflicting_class_groups
    assert result["conflicting_class_groups"]["toOverride"] == ["groupOverridden"]
    assert result["conflicting_class_groups"]["fooKey"] == ["otherKey"]
    assert result["conflicting_class_groups"]["otherKey"] == ["fooKey", "fooKey2"]
    
    # Check conflicting_class_group_modifiers
    assert "hello" in result["conflicting_class_group_modifiers"]
    assert "world" in result["conflicting_class_group_modifiers"]["hello"]
    assert "world2" in result["conflicting_class_group_modifiers"]["hello"]
    assert result["conflicting_class_group_modifiers"]["toOverride"] == ["overridden-2"]
    
    # Check order_sensitive_modifiers - should exactly match TypeScript expected array
    assert result["order_sensitive_modifiers"] == ["order-2", "order-3"]