"""
tailwind-merge Python port.

This library provides utilities for merging Tailwind CSS classes,
handling conflicts according to the configured rules.
"""

# Import core API functions
from tw_merge.lib.create_tailwind_merge import create_tailwind_merge
from tw_merge.lib.tw_join import tw_join, ClassNameValue
from tw_merge.lib.default_config import get_default_config
from tw_merge.lib.tw_merge import tailwind_merge, tw_merge
from tw_merge.lib.extend_tailwind_merge import extend_tailwind_merge
from tw_merge.lib.merge_configs import merge_configs
from tw_merge.lib.from_theme import from_theme

# Import validators module
from tw_merge.lib import validators

# Re-export validator functions commonly used in tests
from tw_merge.lib.validators import (
    is_arbitrary_value,
    is_length,
    is_tshirt_size,
    is_any,
    is_color,
    is_number,
    is_integer,
    is_percent,
    is_arbitrary_number,
    is_arbitrary_length,
    is_arbitrary_position,
    is_arbitrary_size,
    is_arbitrary_shadow,
    is_arbitrary_image,
    is_arbitrary_variable,
    is_arbitrary_variable_family_name,
    is_arbitrary_variable_image,
    is_arbitrary_variable_length,
    is_arbitrary_variable_position,
    is_arbitrary_variable_shadow,
    is_arbitrary_variable_size,
    is_fraction,
    is_image,
    is_shadow,
    is_never,
    is_any_non_arbitrary,
)

# Import parse_class_name and constants
from tw_merge.lib.parse_class_name import create_parse_class_name, IMPORTANT_MODIFIER

__all__ = [
    'create_tailwind_merge',
    'tw_join',
    'ClassNameValue',
    'get_default_config',
    'tailwind_merge',
    'tw_merge',
    'extend_tailwind_merge',
    'merge_configs',
    'from_theme',
    'validators',
    'is_arbitrary_value',
    'is_length',
    'is_tshirt_size',
    'is_any',
    'is_color',
    'is_number',
    'is_integer',
    'is_percent',
    'is_arbitrary_number',
    'is_arbitrary_length',
    'is_arbitrary_position',
    'is_arbitrary_size',
    'is_arbitrary_shadow',
    'is_arbitrary_image',
    'is_arbitrary_variable',
    'is_arbitrary_variable_family_name',
    'is_arbitrary_variable_image',
    'is_arbitrary_variable_length',
    'is_arbitrary_variable_position',
    'is_arbitrary_variable_shadow',
    'is_arbitrary_variable_size',
    'is_fraction',
    'is_image',
    'is_shadow',
    'is_never',
    'is_any_non_arbitrary',
    'create_parse_class_name',
    'IMPORTANT_MODIFIER',
]
