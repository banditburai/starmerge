from starmerge import (
    extend_tailwind_merge,
    from_theme,
    get_default_config,
    merge_configs,
)


def test_extendtailwindmerge_type_generics_work_correctly():
    tailwind_merge1 = extend_tailwind_merge(
        {
            "extend": {
                "theme": {
                    "spacing": ["my-space"],
                    "plll": ["something"],
                },
                "class_groups": {
                    "px": ["px-foo"],
                    "pxx": ["pxx-foo"],
                },
                "conflicting_class_groups": {
                    "px": ["p"],
                    "pxx": ["p"],
                },
                "conflicting_class_group_modifiers": {
                    "p": ["px", "prr"],
                },
            },
        }
    )

    assert tailwind_merge1("") == ""

    tailwind_merge2 = extend_tailwind_merge(
        {
            "extend": {
                "theme": {
                    "spacing": ["my-space"],
                    "plll": ["something"],
                    "test3": ["bar"],
                },
                "class_groups": {
                    "px": ["px-foo"],
                    "pxx": ["pxx-foo"],
                    "test1": ["foo"],
                    "test2": ["bar"],
                },
                "conflicting_class_groups": {
                    "px": ["p"],
                    "pxx": ["p"],
                    "test1": ["test2"],
                },
                "conflicting_class_group_modifiers": {
                    "p": ["px", "prr", "test2", "test1"],
                    "test1": ["test2"],
                },
            },
        }
    )

    assert tailwind_merge2("") == ""

    tailwind_merge3 = extend_tailwind_merge(lambda v: v, get_default_config)

    assert tailwind_merge3("") == ""


def test_fromtheme_type_generics_work_correctly():
    theme_validator = from_theme("test4")
    assert callable(theme_validator)


def test_mergeconfigs_type_generics_work_correctly():
    config1 = merge_configs(
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
            "order_sensitive_modifiers": [],
        },
        {
            "override": {
                "theme": {
                    "baz": [],
                    "nope": [],
                },
                "class_groups": {
                    "foo": [],
                    "bar": [],
                    "hiii": [],
                },
                "conflicting_class_groups": {
                    "foo": ["bar", "lol"],
                },
                "conflicting_class_group_modifiers": {
                    "bar": ["foo"],
                    "lel": ["foo"],
                },
            },
            "extend": {
                "class_groups": {
                    "foo": [],
                    "bar": [],
                    "hiii": [],
                },
                "conflicting_class_groups": {
                    "foo": ["bar", "lol"],
                },
                "conflicting_class_group_modifiers": {
                    "bar": ["foo"],
                    "lel": ["foo"],
                },
            },
        },
    )

    assert isinstance(config1, dict)

    config2 = merge_configs(get_default_config(), {})
    assert isinstance(config2, dict)

    config3 = merge_configs(get_default_config(), {})
    assert isinstance(config3, dict)
