from starmerge import create_tailwind_merge


def test_createtailwindmerge_works_with_single_config_function():
    def config_fn():
        return {
            "cache_size": 20,
            "theme": {},
            "class_groups": {
                "fooKey": [{"fooKey": ["bar", "baz"]}],
                "fooKey2": [{"fooKey": ["qux", "quux"]}, "other-2"],
                "otherKey": ["nother", "group"],
            },
            "conflicting_class_groups": {
                "fooKey": ["otherKey"],
                "otherKey": ["fooKey", "fooKey2"],
            },
            "conflicting_class_group_modifiers": {},
            "order_sensitive_modifiers": [],
        }
    
    tailwind_merge = create_tailwind_merge(config_fn)
    
    assert tailwind_merge('') == ''
    assert tailwind_merge('my-modifier:fooKey-bar my-modifier:fooKey-baz') == 'my-modifier:fooKey-baz'
    assert tailwind_merge('other-modifier:fooKey-bar other-modifier:fooKey-baz') == 'other-modifier:fooKey-baz'
    assert tailwind_merge('group fooKey-bar') == 'fooKey-bar'
    assert tailwind_merge('fooKey-bar group') == 'group'
    assert tailwind_merge('group other-2') == 'group other-2'
    assert tailwind_merge('other-2 group') == 'group'


def test_createtailwindmerge_works_with_multiple_config_functions():
    def first_config_fn():
        return {
            "cache_size": 20,
            "theme": {},
            "class_groups": {
                "fooKey": [{"fooKey": ["bar", "baz"]}],
                "fooKey2": [{"fooKey": ["qux", "quux"]}, "other-2"],
                "otherKey": ["nother", "group"],
            },
            "conflicting_class_groups": {
                "fooKey": ["otherKey"],
                "otherKey": ["fooKey", "fooKey2"],
            },
            "conflicting_class_group_modifiers": {},
            "order_sensitive_modifiers": [],
        }
    
    def second_config_fn(config):
        return {
            **config,
            "class_groups": {
                **config["class_groups"],
                "helloFromSecondConfig": ["hello-there"],
            },
            "conflicting_class_groups": {
                **config["conflicting_class_groups"],
                "fooKey": [*(config["conflicting_class_groups"].get("fooKey", [])), "helloFromSecondConfig"],
            },
        }
    
    tailwind_merge = create_tailwind_merge(first_config_fn, second_config_fn)
    
    assert tailwind_merge('') == ''
    assert tailwind_merge('my-modifier:fooKey-bar my-modifier:fooKey-baz') == 'my-modifier:fooKey-baz'
    assert tailwind_merge('other-modifier:fooKey-bar other-modifier:fooKey-baz') == 'other-modifier:fooKey-baz'
    assert tailwind_merge('group fooKey-bar') == 'fooKey-bar'
    assert tailwind_merge('fooKey-bar group') == 'group'
    assert tailwind_merge('group other-2') == 'group other-2'
    assert tailwind_merge('other-2 group') == 'group'
    
    assert tailwind_merge('second:group second:nother') == 'second:nother'
    
    assert tailwind_merge('fooKey-bar hello-there') == 'fooKey-bar hello-there'
    
    assert tailwind_merge('hello-there fooKey-bar') == 'fooKey-bar' 
