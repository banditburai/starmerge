"""
Python equivalent of js-source/arbitrary-variants.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.
"""

import pytest
from starmerge import merge


def test_basic_arbitrary_variants():
    """Equivalent to the 'basic arbitrary variants' test in TypeScript."""
    assert merge('[p]:underline [p]:line-through') == '[p]:line-through'
    assert merge('[&>*]:underline [&>*]:line-through') == '[&>*]:line-through'
    assert merge('[&>*]:underline [&>*]:line-through [&_div]:line-through') == '[&>*]:line-through [&_div]:line-through'
    assert merge('supports-[display:grid]:flex supports-[display:grid]:grid') == 'supports-[display:grid]:grid'


def test_arbitrary_variants_with_modifiers():
    """Equivalent to the 'arbitrary variants with modifiers' test in TypeScript."""
    assert merge('dark:lg:hover:[&>*]:underline dark:lg:hover:[&>*]:line-through') == 'dark:lg:hover:[&>*]:line-through'
    assert merge('dark:lg:hover:[&>*]:underline dark:hover:lg:[&>*]:line-through') == 'dark:hover:lg:[&>*]:line-through'
    # Whether a modifier is before or after arbitrary variant matters
    assert merge('hover:[&>*]:underline [&>*]:hover:line-through') == 'hover:[&>*]:underline [&>*]:hover:line-through'
    assert merge('hover:dark:[&>*]:underline dark:hover:[&>*]:underline dark:[&>*]:hover:line-through') == 'dark:hover:[&>*]:underline dark:[&>*]:hover:line-through'


def test_arbitrary_variants_with_complex_syntax_in_them():
    """Equivalent to the 'arbitrary variants with complex syntax in them' test in TypeScript."""
    assert merge('[@media_screen{@media(hover:hover)}]:underline [@media_screen{@media(hover:hover)}]:line-through') == '[@media_screen{@media(hover:hover)}]:line-through'
    assert merge('hover:[@media_screen{@media(hover:hover)}]:underline hover:[@media_screen{@media(hover:hover)}]:line-through') == 'hover:[@media_screen{@media(hover:hover)}]:line-through'


def test_arbitrary_variants_with_attribute_selectors():
    """Equivalent to the 'arbitrary variants with attribute selectors' test in TypeScript."""
    assert merge('[&[data-open]]:underline [&[data-open]]:line-through') == '[&[data-open]]:line-through'


def test_arbitrary_variants_with_multiple_attribute_selectors():
    """Equivalent to the 'arbitrary variants with multiple attribute selectors' test in TypeScript."""
    assert merge('[&[data-foo][data-bar]:not([data-baz])]:underline [&[data-foo][data-bar]:not([data-baz])]:line-through') == '[&[data-foo][data-bar]:not([data-baz])]:line-through'


def test_multiple_arbitrary_variants():
    """Equivalent to the 'multiple arbitrary variants' test in TypeScript."""
    assert merge('[&>*]:[&_div]:underline [&>*]:[&_div]:line-through') == '[&>*]:[&_div]:line-through'
    assert merge('[&>*]:[&_div]:underline [&_div]:[&>*]:line-through') == '[&>*]:[&_div]:underline [&_div]:[&>*]:line-through'
    assert merge('hover:dark:[&>*]:focus:disabled:[&_div]:underline dark:hover:[&>*]:disabled:focus:[&_div]:line-through') == 'dark:hover:[&>*]:disabled:focus:[&_div]:line-through'
    assert merge('hover:dark:[&>*]:focus:[&_div]:disabled:underline dark:hover:[&>*]:disabled:focus:[&_div]:line-through') == 'hover:dark:[&>*]:focus:[&_div]:disabled:underline dark:hover:[&>*]:disabled:focus:[&_div]:line-through'


def test_arbitrary_variants_with_arbitrary_properties():
    """Equivalent to the 'arbitrary variants with arbitrary properties' test in TypeScript."""
    assert merge('[&>*]:[color:red] [&>*]:[color:blue]') == '[&>*]:[color:blue]'
    assert merge('[&[data-foo][data-bar]:not([data-baz])]:nod:noa:[color:red] [&[data-foo][data-bar]:not([data-baz])]:noa:nod:[color:blue]') == '[&[data-foo][data-bar]:not([data-baz])]:noa:nod:[color:blue]' 