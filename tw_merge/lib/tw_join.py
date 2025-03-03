"""
The code in this file is ported from https://github.com/lukeed/clsx and modified to suit the needs of tailwind-merge better.

Specifically:
- Runtime code from https://github.com/lukeed/clsx/blob/v1.2.1/src/index.js
- TypeScript types from https://github.com/lukeed/clsx/blob/v1.2.1/clsx.d.ts

Original code has MIT license: Copyright (c) Luke Edwards <luke.edwards05@gmail.com> (lukeed.com)
"""

from typing import List, Union, Optional, Any

# Define ClassNameValue type similar to TypeScript original
ClassNameArray = List['ClassNameValue']
ClassNameValue = Union[ClassNameArray, str, None, bool, int]


def tw_join(*class_lists: ClassNameValue) -> str:
    """
    Join multiple class lists into a single string.
    
    Accepts any number of arguments and joins them into a space-separated string.
    - Falsy values are ignored
    - Arrays are recursively processed
    - String values are added as-is
    
    Examples:
    >>> tw_join('foo', 'bar')
    'foo bar'
    >>> tw_join(['foo', None, 'bar'])
    'foo bar'
    >>> tw_join('foo', ['bar', ['baz']])
    'foo bar baz'
    >>> tw_join('grow', [None, False, [['grow-[2]']]])
    'grow grow-[2]'
    """
    result = []
    
    for argument in class_lists:
        if argument:
            # Process each argument, which could be a string or list
            value = to_value(argument)
            if value:
                result.append(value)
                
    return ' '.join(result)


def to_value(mix: Any) -> str:
    """
    Convert a class name value or array to a string.
    
    Args:
        mix: A string, array, or other value to convert
        
    Returns:
        A space-separated string of class names
    """
    # Handle strings directly
    if isinstance(mix, str):
        return mix
        
    # Handle non-lists and falsy values
    if not isinstance(mix, list):
        return ''
    
    result = []
    
    # Handle arrays (including nested arrays)
    for item in mix:
        # Skip falsy values (None, False, empty string, etc.)
        if not item:
            continue
            
        # Recursively process nested arrays or convert non-array items
        if isinstance(item, list):
            value = to_value(item)
        elif isinstance(item, str):
            value = item
        else:
            # Convert non-string primitives to strings
            value = str(item)
            
        if value:
            result.append(value)
                
    return ' '.join(result)
