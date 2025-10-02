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
    result = []

    for argument in class_lists:
        if argument:
            value = to_value(argument)
            if value:
                result.append(value)

    return ' '.join(result)


def to_value(mix: Any) -> str:
    if isinstance(mix, str):
        return mix

    if not isinstance(mix, list):
        return ''

    result = []

    for item in mix:
        if not item:
            continue

        if isinstance(item, list):
            value = to_value(item)
        elif isinstance(item, str):
            value = item
        else:
            value = str(item)

        if value:
            result.append(value)

    return ' '.join(result)
