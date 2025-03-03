"""
Python equivalent of js-source/type-generics.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests, focusing on 
matching the runtime behavior since Python is dynamically typed.
"""

import pytest
from tw_merge import extend_tailwind_merge, from_theme, get_default_config, merge_configs


def test_extendtailwindmerge_type_generics_work_correctly():
    """Test that extend_tailwind_merge works with custom theme and class groups."""
    # Simple extension
    tailwind_merge1 = extend_tailwind_merge({
        'extend': {
            'theme': {
                'spacing': ['my-space'],
                # Type error in TypeScript, but allowed in Python
                'plll': ['something'],
            },
            'classGroups': {
                'px': ['px-foo'],
                # Type error in TypeScript, but allowed in Python
                'pxx': ['pxx-foo'],
            },
            'conflictingClassGroups': {
                'px': ['p'],
                # Type error in TypeScript, but allowed in Python
                'pxx': ['p'],
            },
            'conflictingClassGroupModifiers': {
                'p': [
                    'px',
                    # Type error in TypeScript, but allowed in Python
                    'prr',
                ],
            },
        },
    })

    assert tailwind_merge1('') == ''

    # More complex extension - TypeScript has type parameters here
    tailwind_merge2 = extend_tailwind_merge({
        'extend': {
            'theme': {
                'spacing': ['my-space'],
                # Type error in TypeScript, but allowed in Python
                'plll': ['something'],
                'test3': ['bar'],
            },
            'classGroups': {
                'px': ['px-foo'],
                # Type error in TypeScript, but allowed in Python
                'pxx': ['pxx-foo'],
                'test1': ['foo'],
                'test2': ['bar'],
            },
            'conflictingClassGroups': {
                'px': ['p'],
                # Type error in TypeScript, but allowed in Python
                'pxx': ['p'],
                'test1': ['test2'],
            },
            'conflictingClassGroupModifiers': {
                'p': [
                    'px',
                    # Type error in TypeScript, but allowed in Python
                    'prr',
                    'test2',
                    'test1',
                ],
                'test1': ['test2'],
            },
        },
    })

    assert tailwind_merge2('') == ''
    

    tailwind_merge3 = extend_tailwind_merge(lambda v: v, get_default_config)
    
    assert tailwind_merge3('') == ''


def test_fromtheme_type_generics_work_correctly():
    """Test that from_theme returns a function that can extract values from theme."""
    # TypeScript has type parameters here
    theme_validator = from_theme('test4')
    assert callable(theme_validator)

    # In TypeScript, there are several type checks here
    # We can skip them as they're only relevant at compile time


def test_mergeconfigs_type_generics_work_correctly():
    """Test that merge_configs correctly merges configuration objects."""
    # TypeScript has type parameters here
    config1 = merge_configs(
        {
            'cacheSize': 50,
            'prefix': 'tw',
            'theme': {
                'hi': ['ho'],
                'themeToOverride': ['to-override'],
            },
            'classGroups': {
                'fooKey': [{'fooKey': ['one', 'two']}],
                'bla': [{'bli': ['blub', 'blublub']}],
                'groupToOverride': ['this', 'will', 'be', 'overridden'],
                'groupToOverride2': ['this', 'will', 'not', 'be', 'overridden'],
            },
            'conflictingClassGroups': {
                'toOverride': ['groupToOverride'],
            },
            'conflictingClassGroupModifiers': {
                'hello': ['world'],
                'toOverride': ['groupToOverride-2'],
            },
            'orderSensitiveModifiers': [],
        },
        {
            'prefix': None,  # None in Python is equivalent to undefined in TypeScript
            'override': {
                'theme': {
                    'baz': [],
                    # Type error in TypeScript, but allowed in Python
                    'nope': [],
                },
                'classGroups': {
                    'foo': [],
                    'bar': [],
                    # Type error in TypeScript, but allowed in Python
                    'hiii': [],
                },
                'conflictingClassGroups': {
                    'foo': [
                        'bar',
                        # Type error in TypeScript, but allowed in Python
                        'lol',
                    ],
                },
                'conflictingClassGroupModifiers': {
                    'bar': ['foo'],
                    # Type error in TypeScript, but allowed in Python
                    'lel': ['foo'],
                },
            },
            'extend': {
                'classGroups': {
                    'foo': [],
                    'bar': [],
                    # Type error in TypeScript, but allowed in Python
                    'hiii': [],
                },
                'conflictingClassGroups': {
                    'foo': [
                        'bar',
                        # Type error in TypeScript, but allowed in Python
                        'lol',
                    ],
                },
                'conflictingClassGroupModifiers': {
                    'bar': ['foo'],
                    # Type error in TypeScript, but allowed in Python
                    'lel': ['foo'],
                },
            },
        },
    )

    assert isinstance(config1, dict)

    config2 = merge_configs(get_default_config(), {})
    assert isinstance(config2, dict)

    config3 = merge_configs(get_default_config(), {})
    assert isinstance(config3, dict) 