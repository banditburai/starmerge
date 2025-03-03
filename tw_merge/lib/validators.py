"""
Validators for tailwind-merge.

This module provides functions to validate different types of Tailwind CSS class values,
including arbitrary values, fractions, numbers, percentages, and more.
"""

import re
from typing import Callable, Set, Optional, TypeAlias

# Regular expression patterns for different types of values
arbitrary_value_regex = re.compile(r'^\[(?:(\w[\w-]*):)?(.+)\]$', re.IGNORECASE)
arbitrary_variable_regex = re.compile(r'^\((?:(\w[\w-]*):)?(.+)\)$', re.IGNORECASE)
fraction_regex = re.compile(r'^\d+\/\d+$')
tshirt_unit_regex = re.compile(r'^(\d+(\.\d+)?)?(xs|sm|md|lg|xl)$')
length_unit_regex = re.compile(
    r'\d+(%|px|r?em|[sdl]?v([hwib]|min|max)|pt|pc|in|cm|mm|cap|ch|ex|r?lh|cq(w|h|i|b|min|max))|\b(calc|min|max|clamp)\(.+\)$'
)
color_function_regex = re.compile(r'^(rgba?|hsla?|hwb|(ok)?(lab|lch))\(.+\)$')
# Shadow always begins with x and y offset separated by underscore optionally prepended by inset
shadow_regex = re.compile(r'^(inset_)?-?((\d+)?\.?(\d+)[a-z]+|0)_-?((\d+)?\.?(\d+)[a-z]+|0)')
image_regex = re.compile(
    r'^(url|image|image-set|cross-fade|element|(repeating-)?(linear|radial|conic)-gradient)\(.+\)$'
)

# Type alias for validators
ClassValidator: TypeAlias = Callable[[str], bool]


def is_fraction(value: str) -> bool:
    """Check if value is a fraction (e.g., '1/2')."""
    return bool(fraction_regex.match(value))


def is_number(value: str) -> bool:
    """Check if value is a number."""
    if not value:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_integer(value: str) -> bool:
    """Check if value is an integer."""
    if not value:
        return False
    
    # Handle decimal numbers that are whole numbers (e.g., 10.0)
    if '.' in value:
        try:
            # Check if it's a whole number (e.g., 10.0)
            num = float(value)
            return num.is_integer()
        except ValueError:
            return False
    
    # Handle negative numbers
    if value.startswith('-'):
        return value[1:].isdigit() and not any(c.isspace() for c in value)
    
    return value.isdigit() and not any(c.isspace() for c in value)


def is_percent(value: str) -> bool:
    """Check if value is a percentage."""
    return (not any(c.isspace() for c in value)) and value.endswith('%') and is_number(value[:-1])


def is_tshirt_size(value: str) -> bool:
    """Check if value is a t-shirt size (e.g., 'sm', 'md', 'lg')."""
    return bool(tshirt_unit_regex.match(value))


def is_any(_: str = None) -> bool:
    """Always return True for any value."""
    return True


def is_length_only(value: str) -> bool:
    """
    Check if value is a length (e.g., '10px', '2rem') but not a color function.
    
    `color_function_regex` check is necessary because color functions can have percentages
    in them which would be incorrectly classified as lengths.
    For example, `hsl(0 0% 0%)` would be classified as a length without this check.
    """
    # Handle special values explicitly
    if value in ['px', 'full', 'screen', '0']:
        return True
    
    return bool(length_unit_regex.search(value)) and not bool(color_function_regex.match(value))


def is_length(value: str) -> bool:
    """
    Check if value is a length (e.g., '10px', '2rem') or a percentage.
    
    This is a combination of is_length_only and is_percent.
    """
    return is_length_only(value) or is_percent(value)


def is_color(value: str) -> bool:
    """
    Check if value is a color.
    
    This includes color function notation (e.g., 'rgb()', 'hsl()')
    and hex colors (e.g., '#fff', '#abcdef').
    """
    if not value:
        return False
    
    # Check for color functions like rgb(), hsl()
    if color_function_regex.match(value):
        return True
    
    # Check for hex colors (3, 4, 6, or 8 characters after #)
    if value.startswith('#') and len(value) in [4, 5, 7, 9]:
        try:
            # Remove the # and try to parse as a hex number
            int(value[1:], 16)
            return True
        except ValueError:
            return False
    
    return False


def is_never(_: str = None) -> bool:
    """Always return False for any value."""
    return False


def is_shadow(value: str) -> bool:
    """Check if value is a shadow value."""
    return bool(shadow_regex.match(value))


def is_image(value: str) -> bool:
    """Check if value is an image value."""
    return bool(image_regex.match(value))


def is_any_non_arbitrary(value: str) -> bool:
    """Check if value is not an arbitrary value or variable."""
    return not is_arbitrary_value(value) and not is_arbitrary_variable(value)


def is_arbitrary_size(value: str) -> bool:
    """Check if value is an arbitrary size."""
    return get_is_arbitrary_value(value, is_label_size, is_never)


def is_arbitrary_value(value: str) -> bool:
    """Check if value is an arbitrary value, enclosed in square brackets."""
    return bool(arbitrary_value_regex.match(value))


def is_arbitrary_length(value: str) -> bool:
    """Check if value is an arbitrary length."""
    return get_is_arbitrary_value(value, is_label_length, is_length_only)


def is_arbitrary_number(value: str) -> bool:
    """Check if value is an arbitrary number."""
    return get_is_arbitrary_value(value, is_label_number, is_number)


def is_arbitrary_position(value: str) -> bool:
    """Check if value is an arbitrary position."""
    return get_is_arbitrary_value(value, is_label_position, is_never)


def is_arbitrary_image(value: str) -> bool:
    """Check if value is an arbitrary image."""
    return get_is_arbitrary_value(value, is_label_image, is_image)


def is_arbitrary_shadow(value: str) -> bool:
    """Check if value is an arbitrary shadow."""
    return get_is_arbitrary_value(value, is_never, is_shadow)


def is_arbitrary_variable(value: str) -> bool:
    """Check if value is an arbitrary variable, enclosed in parentheses."""
    return bool(arbitrary_variable_regex.match(value))


def is_arbitrary_variable_length(value: str) -> bool:
    """Check if value is an arbitrary variable length."""
    return get_is_arbitrary_variable(value, is_label_length)


def is_arbitrary_variable_family_name(value: str) -> bool:
    """Check if value is an arbitrary variable family name."""
    return get_is_arbitrary_variable(value, is_label_family_name)


def is_arbitrary_variable_position(value: str) -> bool:
    """Check if value is an arbitrary variable position."""
    return get_is_arbitrary_variable(value, is_label_position)


def is_arbitrary_variable_size(value: str) -> bool:
    """Check if value is an arbitrary variable size."""
    return get_is_arbitrary_variable(value, is_label_size)


def is_arbitrary_variable_image(value: str) -> bool:
    """Check if value is an arbitrary variable image."""
    return get_is_arbitrary_variable(value, is_label_image)


def is_arbitrary_variable_shadow(value: str) -> bool:
    """Check if value is an arbitrary variable shadow."""
    return get_is_arbitrary_variable(value, is_label_shadow, True)


# Helper functions

def get_is_arbitrary_value(
    value: str,
    test_label: Callable[[str], bool],
    test_value: Callable[[str], bool],
) -> bool:
    """
    Check if value is an arbitrary value with a specific label or matching a specific test.
    
    Args:
        value: The value to test
        test_label: Function to test the label part of the arbitrary value
        test_value: Function to test the value part of the arbitrary value
        
    Returns:
        True if the value is an arbitrary value matching the criteria, False otherwise
    """
    match = arbitrary_value_regex.match(value)
    
    if match:
        if match.group(1):
            return test_label(match.group(1))
        
        return test_value(match.group(2))
    
    return False


def get_is_arbitrary_variable(
    value: str,
    test_label: Callable[[str], bool],
    should_match_no_label: bool = False,
) -> bool:
    """
    Check if value is an arbitrary variable with a specific label.
    
    Args:
        value: The value to test
        test_label: Function to test the label part of the arbitrary variable
        should_match_no_label: Whether to match variables without a label
        
    Returns:
        True if the value is an arbitrary variable matching the criteria, False otherwise
    """
    match = arbitrary_variable_regex.match(value)
    
    if match:
        if match.group(1):
            return test_label(match.group(1))
        return should_match_no_label
    
    return False


# Label validators

def is_label_position(label: str) -> bool:
    """Check if label is 'position'."""
    return label == 'position'


# Sets for label types
image_labels: Set[str] = {'image', 'url'}


def is_label_image(label: str) -> bool:
    """Check if label is an image label."""
    return label in image_labels


size_labels: Set[str] = {'length', 'size', 'percentage'}


def is_label_size(label: str) -> bool:
    """Check if label is a size label."""
    return label in size_labels


def is_label_length(label: str) -> bool:
    """Check if label is 'length'."""
    return label == 'length'


def is_label_number(label: str) -> bool:
    """Check if label is 'number'."""
    return label == 'number'


def is_label_family_name(label: str) -> bool:
    """Check if label is 'family-name'."""
    return label == 'family-name'


def is_label_shadow(label: str) -> bool:
    """Check if label is 'shadow'."""
    return label == 'shadow'
