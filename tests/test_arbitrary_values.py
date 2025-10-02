"""
Python equivalent of js-source/arbitrary-values.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.
"""

import pytest
from starmerge import merge


def test_handles_simple_conflicts_with_arbitrary_values_correctly():
    """Equivalent to the 'handles simple conflicts with arbitrary values correctly' test in TypeScript."""
    assert merge('m-[2px] m-[10px]') == 'm-[10px]'
    assert merge(
        'm-[2px] m-[11svmin] m-[12in] m-[13lvi] m-[14vb] m-[15vmax] m-[16mm] m-[17%] m-[18em] m-[19px] m-[10dvh]'
    ) == 'm-[10dvh]'
    assert merge(
        'h-[10px] h-[11cqw] h-[12cqh] h-[13cqi] h-[14cqb] h-[15cqmin] h-[16cqmax]'
    ) == 'h-[16cqmax]'
    assert merge('z-20 z-[99]') == 'z-[99]'
    assert merge('my-[2px] m-[10rem]') == 'm-[10rem]'
    assert merge('cursor-pointer cursor-[grab]') == 'cursor-[grab]'
    assert merge('m-[2px] m-[calc(100%-var(--arbitrary))]') == 'm-[calc(100%-var(--arbitrary))]'
    assert merge('m-[2px] m-[length:var(--mystery-var)]') == 'm-[length:var(--mystery-var)]'
    assert merge('opacity-10 opacity-[0.025]') == 'opacity-[0.025]'
    assert merge('scale-75 scale-[1.7]') == 'scale-[1.7]'
    assert merge('brightness-90 brightness-[1.75]') == 'brightness-[1.75]'

    # Handling of value `0`
    assert merge('min-h-[0.5px] min-h-[0]') == 'min-h-[0]'
    assert merge('text-[0.5px] text-[color:0]') == 'text-[0.5px] text-[color:0]'
    assert merge('text-[0.5px] text-(--my-0)') == 'text-[0.5px] text-(--my-0)'


def test_handles_arbitrary_length_conflicts_with_labels_and_modifiers_correctly():
    """Equivalent to the 'handles arbitrary length conflicts with labels and modifiers correctly' test in TypeScript."""
    assert merge('hover:m-[2px] hover:m-[length:var(--c)]') == 'hover:m-[length:var(--c)]'
    assert merge('hover:focus:m-[2px] focus:hover:m-[length:var(--c)]') == 'focus:hover:m-[length:var(--c)]'
    assert merge('border-b border-[color:rgb(var(--color-gray-500-rgb)/50%))]') == 'border-b border-[color:rgb(var(--color-gray-500-rgb)/50%))]'
    assert merge('border-[color:rgb(var(--color-gray-500-rgb)/50%))] border-b') == 'border-[color:rgb(var(--color-gray-500-rgb)/50%))] border-b'
    assert merge('border-b border-[color:rgb(var(--color-gray-500-rgb)/50%))] border-some-coloooor') == 'border-b border-some-coloooor'


def test_handles_complex_arbitrary_value_conflicts_correctly():
    """Equivalent to the 'handles complex arbitrary value conflicts correctly' test in TypeScript."""
    assert merge('grid-rows-[1fr,auto] grid-rows-2') == 'grid-rows-2'
    assert merge('grid-rows-[repeat(20,minmax(0,1fr))] grid-rows-3') == 'grid-rows-3'


def test_handles_ambiguous_arbitrary_values_correctly():
    """Equivalent to the 'handles ambiguous arbitrary values correctly' test in TypeScript."""
    assert merge('mt-2 mt-[calc(theme(fontSize.4xl)/1.125)]') == 'mt-[calc(theme(fontSize.4xl)/1.125)]'
    assert merge('p-2 p-[calc(theme(fontSize.4xl)/1.125)_10px]') == 'p-[calc(theme(fontSize.4xl)/1.125)_10px]'
    assert merge('mt-2 mt-[length:theme(someScale.someValue)]') == 'mt-[length:theme(someScale.someValue)]'
    assert merge('mt-2 mt-[theme(someScale.someValue)]') == 'mt-[theme(someScale.someValue)]'
    assert merge('text-2xl text-[length:theme(someScale.someValue)]') == 'text-[length:theme(someScale.someValue)]'
    assert merge('text-2xl text-[calc(theme(fontSize.4xl)/1.125)]') == 'text-[calc(theme(fontSize.4xl)/1.125)]'
    assert merge('bg-cover bg-[percentage:30%] bg-[length:200px_100px]') == 'bg-[length:200px_100px]'
    assert merge('bg-none bg-[url(.)] bg-[image:.] bg-[url:.] bg-[linear-gradient(.)] bg-linear-to-r') == 'bg-linear-to-r'


def test_handles_arbitrary_custom_properties_correctly():
    """Equivalent to the 'handles arbitrary custom properties correctly' test in TypeScript."""
    assert merge('bg-red bg-(--other-red) bg-bottom bg-(position:-my-pos)') == 'bg-(--other-red) bg-(position:-my-pos)'
    assert merge('shadow-xs shadow-(shadow:--something) shadow-red shadow-(--some-other-shadow) shadow-(color:--some-color)') == 'shadow-(--some-other-shadow) shadow-(color:--some-color)' 