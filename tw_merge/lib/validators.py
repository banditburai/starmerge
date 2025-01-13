import re
from typing import Union, Set, Callable, Optional, Match, Pattern

# Regular expressions should be compiled with proper flags
arbitrary_value_regex: Pattern = re.compile(r'^\[(?:([a-z-]+):)?(.+)\]$', re.IGNORECASE)
fraction_regex: Pattern = re.compile(r'^\d+\/\d+$')
tshirt_unit_regex: Pattern = re.compile(r'^(\d+(\.\d+)?)?(xs|sm|md|lg|xl)$', re.IGNORECASE)
length_unit_regex: Pattern = re.compile(
    r'^\d+(%|px|r?em|[sdl]?v([hwib]|min|max)|pt|pc|in|cm|mm|cap|ch|ex|r?lh|cq(w|h|i|b|min|max))|\b(calc|min|max|clamp)\(.+\)|^0$',
    re.IGNORECASE
)
color_function_regex: Pattern = re.compile(r'^(rgba?|hsla?|hwb|(ok)?(lab|lch))\(.+\)$', re.IGNORECASE)
shadow_regex: Pattern = re.compile(
    r'^(inset_)?-?((\d+)?\.?(\d+)[a-z]+|0)_-?((\d+)?\.?(\d+)[a-z]+|0)',
    re.IGNORECASE
)
image_regex: Pattern = re.compile(
    r'^(url|image|image-set|cross-fade|element|(repeating-)?(linear|radial|conic)-gradient)\(.+\)$',
    re.IGNORECASE
)

# Constants as frozen sets for better performance
string_lengths: frozenset[str] = frozenset({'px', 'full', 'screen'})
size_labels: frozenset[str] = frozenset({'length', 'size', 'percentage'})
image_labels: frozenset[str] = frozenset({'image', 'url'})

def is_length(value: str) -> bool:
    """Check if value is a valid length."""
    return bool(is_number(value) or value in string_lengths or fraction_regex.match(value))

def is_arbitrary_length(value: str) -> bool:
    """Check if value is an arbitrary length."""
    return get_is_arbitrary_value(value, 'length', is_length_only)

def is_number(value: str) -> bool:
    """Check if value is a valid number."""
    if not value:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_arbitrary_number(value: str) -> bool:
    return get_is_arbitrary_value(value, 'number', is_number)

def is_integer(value: str) -> bool:
    if not value:
        return False
    try:
        return float(value).is_integer()
    except ValueError:
        return False

def is_percent(value: str) -> bool:
    return value.endswith('%') and is_number(value[:-1])

def is_arbitrary_value(value: str) -> bool:
    return bool(arbitrary_value_regex.match(value))

def is_tshirt_size(value: str) -> bool:
    return bool(tshirt_unit_regex.match(value))

def is_arbitrary_size(value: str) -> bool:
    return get_is_arbitrary_value(value, size_labels, is_never)

def is_arbitrary_position(value: str) -> bool:
    return get_is_arbitrary_value(value, 'position', is_never)

def is_arbitrary_image(value: str) -> bool:
    return get_is_arbitrary_value(value, image_labels, is_image)

def is_arbitrary_shadow(value: str) -> bool:
    return get_is_arbitrary_value(value, '', is_shadow)

def is_any(_: str) -> bool:
    return True

def get_is_arbitrary_value(
    value: str,
    label: Union[str, Set[str]],
    test_value: Callable[[str], bool]
) -> bool:
    """
    Check if value is an arbitrary value matching the given label and test function.
    
    Args:
        value: The value to test
        label: Expected label or set of labels
        test_value: Function to test the value portion
    """
    match: Optional[Match] = arbitrary_value_regex.match(value)
    if match:
        label_value = match.group(1)
        if label_value:
            return label_value == label if isinstance(label, str) else label_value in label
        return test_value(match.group(2))
    return False

def is_length_only(value: str) -> bool:
    return bool(length_unit_regex.match(value)) and not bool(color_function_regex.match(value))

def is_never(_: str) -> bool:
    return False

def is_shadow(value: str) -> bool:
    return bool(shadow_regex.match(value))

def is_image(value: str) -> bool:
    return bool(image_regex.match(value)) 