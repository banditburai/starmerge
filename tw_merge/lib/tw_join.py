"""
The code in this file is copied from https://github.com/lukeed/clsx and modified to suit the needs of tailwind-merge better.

Specifically:
- Runtime code from https://github.com/lukeed/clsx/blob/v1.2.1/src/index.js
- TypeScript types from https://github.com/lukeed/clsx/blob/v1.2.1/clsx.d.ts

Original code has MIT license: Copyright (c) Luke Edwards <luke.edwards05@gmail.com> (lukeed.com)
"""

from typing import Union, List, Optional

# Match TypeScript types more closely
ClassNameValue = Union[List['ClassNameValue'], str, None, int, bool]
ClassNameArray = List[ClassNameValue]

def tw_join(*class_lists: ClassNameValue) -> str:
    """Join class names together, handling nested arrays and falsy values."""
    string = ''
    
    for argument in class_lists:
        if argument:  # Handles falsy values (None, 0, False)
            resolved_value = to_value(argument)
            if resolved_value:
                if string:
                    string += ' '
                string += resolved_value
    
    return string

def to_value(mix: Union[ClassNameArray, str]) -> str:
    """Convert a mixed value (string or array) to a string."""
    if isinstance(mix, str):
        return mix
    
    if not isinstance(mix, (list, tuple)):
        return str(mix) if mix else ''

    string = ''
    for item in mix:
        if item:  # Handles falsy values
            resolved_value = to_value(item)
            if resolved_value:
                if string:
                    string += ' '
                string += resolved_value
    
    return string