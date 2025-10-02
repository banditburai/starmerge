"""Python port of tailwind-merge for merging Tailwind CSS classes and handling conflicts."""

from starmerge.lib.create_tailwind_merge import create_tailwind_merge
from starmerge.lib.tw_join import tw_join, ClassNameValue
from starmerge.lib.default_config import get_default_config
from starmerge.lib.tw_merge import tailwind_merge, merge
from starmerge.lib.extend_tailwind_merge import extend_tailwind_merge
from starmerge.lib.merge_configs import merge_configs
from starmerge.lib.from_theme import from_theme
from starmerge.lib import validators
from starmerge.lib.validators import (
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
from starmerge.lib.parse_class_name import create_parse_class_name, IMPORTANT_MODIFIER

__all__ = [
    'create_tailwind_merge',
    'tw_join',
    'ClassNameValue',
    'get_default_config',
    'tailwind_merge',
    'merge',
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
