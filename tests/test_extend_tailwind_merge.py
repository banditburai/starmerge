from starmerge import extend_tailwind_merge


def test_extendtailwindmerge_works_correctly_with_single_config():
    tailwind_merge = extend_tailwind_merge(
        {
            "cache_size": 20,
            "extend": {
                "class_groups": {
                    "fooKey": [{"fooKey": ["bar", "baz"]}],
                    "fooKey2": [{"fooKey": ["qux", "quux"]}, "other-2"],
                    "otherKey": ["nother", "group"],
                },
                "conflicting_class_groups": {
                    "fooKey": ["otherKey"],
                    "otherKey": ["fooKey", "fooKey2"],
                },
            },
        }
    )

    assert tailwind_merge("") == ""
    assert (
        tailwind_merge("my-modifier:fooKey-bar my-modifier:fooKey-baz")
        == "my-modifier:fooKey-baz"
    )
    assert (
        tailwind_merge("other-modifier:fooKey-bar other-modifier:fooKey-baz")
        == "other-modifier:fooKey-baz"
    )
    assert tailwind_merge("group fooKey-bar") == "fooKey-bar"
    assert tailwind_merge("fooKey-bar group") == "group"
    assert tailwind_merge("group other-2") == "group other-2"
    assert tailwind_merge("other-2 group") == "group"

    assert tailwind_merge("p-10 p-20") == "p-20"
    assert tailwind_merge("hover:focus:p-10 focus:hover:p-20") == "focus:hover:p-20"


def test_extendtailwindmerge_works_correctly_with_multiple_configs():
    def second_config(config):
        config["class_groups"].update(
            {
                "secondConfigKey": ["hi-there", "hello"],
            }
        )
        return config

    tailwind_merge = extend_tailwind_merge(
        {
            "cache_size": 20,
            "extend": {
                "class_groups": {
                    "fooKey": [{"fooKey": ["bar", "baz"]}],
                    "fooKey2": [{"fooKey": ["qux", "quux"]}, "other-2"],
                    "otherKey": ["nother", "group"],
                },
                "conflicting_class_groups": {
                    "fooKey": ["otherKey"],
                    "otherKey": ["fooKey", "fooKey2"],
                },
            },
        },
        second_config,
    )

    assert tailwind_merge("") == ""
    assert (
        tailwind_merge("my-modifier:fooKey-bar my-modifier:fooKey-baz")
        == "my-modifier:fooKey-baz"
    )
    assert (
        tailwind_merge("other-modifier:hi-there other-modifier:hello")
        == "other-modifier:hello"
    )
    assert tailwind_merge("group fooKey-bar") == "fooKey-bar"
    assert tailwind_merge("fooKey-bar group") == "group"
    assert tailwind_merge("group other-2") == "group other-2"
    assert tailwind_merge("other-2 group") == "group"

    assert tailwind_merge("p-10 p-20") == "p-20"
    assert tailwind_merge("hover:focus:p-10 focus:hover:p-20") == "focus:hover:p-20"


def test_extendtailwindmerge_works_correctly_with_function_config():
    def config_function(config):
        config["cache_size"] = 20
        config["class_groups"].update(
            {
                "fooKey": [{"fooKey": ["bar", "baz"]}],
                "fooKey2": [{"fooKey": ["qux", "quux"]}, "other-2"],
                "otherKey": ["nother", "group"],
            }
        )
        config["conflicting_class_groups"].update(
            {
                "fooKey": ["otherKey"],
                "otherKey": ["fooKey", "fooKey2"],
            }
        )
        return config

    tailwind_merge = extend_tailwind_merge(config_function)

    assert tailwind_merge("") == ""
    assert (
        tailwind_merge("my-modifier:fooKey-bar my-modifier:fooKey-baz")
        == "my-modifier:fooKey-baz"
    )
    assert (
        tailwind_merge("other-modifier:fooKey-bar other-modifier:fooKey-baz")
        == "other-modifier:fooKey-baz"
    )
    assert tailwind_merge("group fooKey-bar") == "fooKey-bar"
    assert tailwind_merge("fooKey-bar group") == "group"
    assert tailwind_merge("group other-2") == "group other-2"
    assert tailwind_merge("other-2 group") == "group"

    assert tailwind_merge("p-10 p-20") == "p-20"
    assert tailwind_merge("hover:focus:p-10 focus:hover:p-20") == "focus:hover:p-20"


def test_extendtailwindmerge_overrides_and_extends_correctly():
    tailwind_merge = extend_tailwind_merge(
        {
            "cache_size": 20,
            "override": {
                "class_groups": {
                    "shadow": ["shadow-100", "shadow-200"],
                    "customKey": ["custom-100"],
                },
                "conflicting_class_groups": {
                    "p": ["px"],
                },
            },
            "extend": {
                "class_groups": {
                    "shadow": ["shadow-300"],
                    "customKey": ["custom-200"],
                    "font-size": ["text-foo"],
                },
                "conflicting_class_groups": {
                    "m": ["h"],
                },
            },
        }
    )

    assert tailwind_merge("shadow-lg shadow-100 shadow-200") == "shadow-lg shadow-200"
    assert tailwind_merge("custom-100 custom-200") == "custom-200"
    assert tailwind_merge("text-lg text-foo") == "text-foo"

    assert tailwind_merge("px-3 py-3 p-3") == "py-3 p-3"
    assert tailwind_merge("p-3 px-3 py-3") == "p-3 px-3 py-3"
    assert tailwind_merge("mx-2 my-2 h-2 m-2") == "m-2"
    assert tailwind_merge("m-2 mx-2 my-2 h-2") == "m-2 mx-2 my-2 h-2"
