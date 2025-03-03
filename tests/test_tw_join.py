"""
Python equivalent of js-source/tw-join.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.

This test file verifies the behavior of the tw_join function, which is based on
the clsx library (https://github.com/lukeed/clsx) and modified for tailwind-merge.
"""

import pytest
from tw_merge import tw_join


def test_strings():
    """Test that tw_join works with string arguments."""
    assert tw_join('') == ''
    assert tw_join('foo') == 'foo'
    assert tw_join(True and 'foo') == 'foo'
    assert tw_join(False and 'foo') == ''


def test_strings_variadic():
    """Test that tw_join works with multiple string arguments."""
    assert tw_join('') == ''
    assert tw_join('foo', 'bar') == 'foo bar'
    assert tw_join(True and 'foo', False and 'bar', 'baz') == 'foo baz'
    assert tw_join(False and 'foo', 'bar', 'baz', '') == 'bar baz'


def test_arrays():
    """Test that tw_join works with array arguments."""
    assert tw_join([]) == ''
    assert tw_join(['foo']) == 'foo'
    assert tw_join(['foo', 'bar']) == 'foo bar'
    assert tw_join(['foo', 0 and 'bar', 1 and 'baz']) == 'foo baz'


def test_arrays_nested():
    """Test that tw_join works with nested array arguments."""
    assert tw_join([[[]]]) == ''
    assert tw_join([[['foo']]]) == 'foo'
    assert tw_join([False, [['foo']]]) == 'foo'
    assert tw_join(['foo', ['bar', ['', [['baz']]]]]) == 'foo bar baz'


def test_arrays_variadic():
    """Test that tw_join works with multiple array arguments."""
    assert tw_join([], []) == ''
    assert tw_join(['foo'], ['bar']) == 'foo bar'
    assert tw_join(['foo'], None, ['baz', ''], False, '', []) == 'foo baz' 