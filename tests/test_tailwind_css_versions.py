"""
Python equivalent of js-source/tailwind-css-versions.test.ts
Last synced with original version: Current (as of implementation)

This test file maintains exact parity with the TypeScript tests to ensure
consistent behavior between the JavaScript and Python implementations.
"""

import pytest
from starmerge import merge


def test_supports_tailwind_css_v3_3_features():
    """Test support for Tailwind CSS v3.3 features."""
    assert merge('text-red text-lg/7 text-lg/8') == 'text-red text-lg/8'
    
    assert merge(
        'start-0 start-1',
        'end-0 end-1',
        'ps-0 ps-1 pe-0 pe-1',
        'ms-0 ms-1 me-0 me-1',
        'rounded-s-sm rounded-s-md rounded-e-sm rounded-e-md',
        'rounded-ss-sm rounded-ss-md rounded-ee-sm rounded-ee-md',
    ) == 'start-1 end-1 ps-1 pe-1 ms-1 me-1 rounded-s-md rounded-e-md rounded-ss-md rounded-ee-md'
    
    assert merge(
        'start-0 end-0 inset-0 ps-0 pe-0 p-0 ms-0 me-0 m-0 rounded-ss rounded-es rounded-s',
    ) == 'inset-0 p-0 m-0 rounded-s'
    
    assert merge('hyphens-auto hyphens-manual') == 'hyphens-manual'
    
    assert merge(
        'from-0% from-10% from-[12.5%] via-0% via-10% via-[12.5%] to-0% to-10% to-[12.5%]'
    ) == 'from-[12.5%] via-[12.5%] to-[12.5%]'
    
    assert merge('from-0% from-red') == 'from-0% from-red'
    
    assert merge(
        'list-image-none list-image-[url(./my-image.png)] list-image-[var(--value)]'
    ) == 'list-image-[var(--value)]'
    
    assert merge('caption-top caption-bottom') == 'caption-bottom'
    assert merge('line-clamp-2 line-clamp-none line-clamp-[10]') == 'line-clamp-[10]'
    assert merge('delay-150 delay-0 duration-150 duration-0') == 'delay-0 duration-0'
    assert merge('justify-normal justify-center justify-stretch') == 'justify-stretch'
    assert merge('content-normal content-center content-stretch') == 'content-stretch'
    assert merge('whitespace-nowrap whitespace-break-spaces') == 'whitespace-break-spaces'


def test_supports_tailwind_css_v3_4_features():
    """Test support for Tailwind CSS v3.4 features."""
    assert merge('h-svh h-dvh w-svw w-dvw') == 'h-dvh w-dvw'
    
    assert merge(
        'has-[[data-potato]]:p-1 has-[[data-potato]]:p-2 group-has-[:checked]:grid group-has-[:checked]:flex'
    ) == 'has-[[data-potato]]:p-2 group-has-[:checked]:flex'
    
    assert merge('text-wrap text-pretty') == 'text-pretty'
    assert merge('w-5 h-3 size-10 w-12') == 'size-10 w-12'
    
    assert merge('grid-cols-2 grid-cols-subgrid grid-rows-5 grid-rows-subgrid') == \
        'grid-cols-subgrid grid-rows-subgrid'
    
    assert merge('min-w-0 min-w-50 min-w-px max-w-0 max-w-50 max-w-px') == 'min-w-px max-w-px'
    
    assert merge('forced-color-adjust-none forced-color-adjust-auto') == \
        'forced-color-adjust-auto'
    
    assert merge('appearance-none appearance-auto') == 'appearance-auto'
    assert merge('float-start float-end clear-start clear-end') == 'float-end clear-end'
    assert merge('*:p-10 *:p-20 hover:*:p-10 hover:*:p-20') == '*:p-20 hover:*:p-20'


def test_supports_tailwind_css_v4_0_features():
    """Test support for Tailwind CSS v4.0 features."""
    assert merge('transform-3d transform-flat') == 'transform-flat'
    
    assert merge('rotate-12 rotate-x-2 rotate-none rotate-y-3') == \
        'rotate-x-2 rotate-none rotate-y-3'
    
    assert merge('perspective-dramatic perspective-none perspective-midrange') == \
        'perspective-midrange'
    
    assert merge('perspective-origin-center perspective-origin-top-left') == \
        'perspective-origin-top-left'
    
    assert merge('bg-linear-to-r bg-linear-45') == 'bg-linear-45'
    assert merge('bg-linear-to-r bg-radial-[something] bg-conic-10') == 'bg-conic-10'
    
    assert merge('ring-4 ring-orange inset-ring inset-ring-3 inset-ring-blue') == \
        'ring-4 ring-orange inset-ring-3 inset-ring-blue'
    
    assert merge('field-sizing-content field-sizing-fixed') == 'field-sizing-fixed'
    assert merge('scheme-normal scheme-dark') == 'scheme-dark'
    
    assert merge('font-stretch-expanded font-stretch-[66.66%] font-stretch-50%') == \
        'font-stretch-50%' 