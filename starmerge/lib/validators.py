"""Validators for Tailwind CSS class values."""

import re
from typing import Callable, Set, Optional, TypeAlias

arbitrary_value_regex = re.compile(r'^\[(?:(\w[\w-]*):)?(.+)\]$', re.IGNORECASE)
arbitrary_variable_regex = re.compile(r'^\((?:(\w[\w-]*):)?(.+)\)$', re.IGNORECASE)
fraction_regex = re.compile(r'^\d+\/\d+$')
tshirt_unit_regex = re.compile(r'^(\d+(\.\d+)?)?(xs|sm|md|lg|xl)$')
length_unit_regex = re.compile(
    r'\d+(%|px|r?em|[sdl]?v([hwib]|min|max)|pt|pc|in|cm|mm|cap|ch|ex|r?lh|cq(w|h|i|b|min|max))|\b(calc|min|max|clamp)\(.+\)$'
)
color_function_regex = re.compile(r'^(rgba?|hsla?|hwb|(ok)?(lab|lch))\(.+\)$')
shadow_regex = re.compile(r'^(inset_)?-?((\d+)?\.?(\d+)[a-z]+|0)_-?((\d+)?\.?(\d+)[a-z]+|0)')
image_regex = re.compile(
    r'^(url|image|image-set|cross-fade|element|(repeating-)?(linear|radial|conic)-gradient)\(.+\)$'
)

ClassValidator: TypeAlias = Callable[[str], bool]


def is_fraction(value: str) -> bool:
    return bool(fraction_regex.match(value))


def is_number(value: str) -> bool:
    if not value:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_integer(value: str) -> bool:
    if not value:
        return False

    if '.' in value:
        try:
            num = float(value)
            return num.is_integer()
        except ValueError:
            return False

    if value.startswith('-'):
        return value[1:].isdigit() and not any(c.isspace() for c in value)

    return value.isdigit() and not any(c.isspace() for c in value)


def is_percent(value: str) -> bool:
    return (not any(c.isspace() for c in value)) and value.endswith('%') and is_number(value[:-1])


def is_tshirt_size(value: str) -> bool:
    return bool(tshirt_unit_regex.match(value))


def is_any(_: str = None) -> bool:
    return True


def is_length_only(value: str) -> bool:
    """
    Check if value is a length but not a color function.
    Color function check prevents hsl(0 0% 0%) from being classified as a length.
    """
    if value in ['px', 'full', 'screen', '0']:
        return True
    return bool(length_unit_regex.search(value)) and not bool(color_function_regex.match(value))


def is_length(value: str) -> bool:
    return is_length_only(value) or is_percent(value)


def is_color(value: str) -> bool:
    if not value:
        return False

    if color_function_regex.match(value):
        return True

    if value.startswith('#') and len(value) in [4, 5, 7, 9]:
        try:
            int(value[1:], 16)
            return True
        except ValueError:
            return False

    return False


def is_never(_: str = None) -> bool:
    return False


def is_shadow(value: str) -> bool:
    return bool(shadow_regex.match(value))


def is_image(value: str) -> bool:
    return bool(image_regex.match(value))


def is_any_non_arbitrary(value: str) -> bool:
    return not is_arbitrary_value(value) and not is_arbitrary_variable(value)


def is_arbitrary_size(value: str) -> bool:
    return get_is_arbitrary_value(value, is_label_size, is_never)


def is_arbitrary_value(value: str) -> bool:
    return bool(arbitrary_value_regex.match(value))


def is_arbitrary_length(value: str) -> bool:
    return get_is_arbitrary_value(value, is_label_length, is_length_only)


def is_arbitrary_number(value: str) -> bool:
    return get_is_arbitrary_value(value, is_label_number, is_number)


def is_arbitrary_position(value: str) -> bool:
    return get_is_arbitrary_value(value, is_label_position, is_never)


def is_arbitrary_image(value: str) -> bool:
    return get_is_arbitrary_value(value, is_label_image, is_image)


def is_arbitrary_shadow(value: str) -> bool:
    return get_is_arbitrary_value(value, is_never, is_shadow)


def is_arbitrary_variable(value: str) -> bool:
    return bool(arbitrary_variable_regex.match(value))


def is_arbitrary_variable_length(value: str) -> bool:
    return get_is_arbitrary_variable(value, is_label_length)


def is_arbitrary_variable_family_name(value: str) -> bool:
    return get_is_arbitrary_variable(value, is_label_family_name)


def is_arbitrary_variable_position(value: str) -> bool:
    return get_is_arbitrary_variable(value, is_label_position)


def is_arbitrary_variable_size(value: str) -> bool:
    return get_is_arbitrary_variable(value, is_label_size)


def is_arbitrary_variable_image(value: str) -> bool:
    return get_is_arbitrary_variable(value, is_label_image)


def is_arbitrary_variable_shadow(value: str) -> bool:
    return get_is_arbitrary_variable(value, is_label_shadow, True)

def get_is_arbitrary_value(
    value: str,
    test_label: Callable[[str], bool],
    test_value: Callable[[str], bool],
) -> bool:
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
    match = arbitrary_variable_regex.match(value)

    if match:
        if match.group(1):
            return test_label(match.group(1))
        return should_match_no_label

    return False


def is_label_position(label: str) -> bool:
    return label == 'position'


image_labels: Set[str] = {'image', 'url'}


def is_label_image(label: str) -> bool:
    return label in image_labels


size_labels: Set[str] = {'length', 'size', 'percentage'}


def is_label_size(label: str) -> bool:
    return label in size_labels


def is_label_length(label: str) -> bool:
    return label == 'length'


def is_label_number(label: str) -> bool:
    return label == 'number'


def is_label_family_name(label: str) -> bool:
    return label == 'family-name'


def is_label_shadow(label: str) -> bool:
    return label == 'shadow'
