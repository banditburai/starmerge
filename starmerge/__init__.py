from importlib.metadata import version

from starmerge.lib import validators
from starmerge.lib.create_tailwind_merge import create_tailwind_merge
from starmerge.lib.default_config import get_default_config
from starmerge.lib.extend_tailwind_merge import extend_tailwind_merge
from starmerge.lib.from_theme import from_theme
from starmerge.lib.merge_configs import merge_configs
from starmerge.lib.parse_class_name import IMPORTANT_MODIFIER, create_parse_class_name
from starmerge.lib.tw_join import ClassNameValue, tw_join
from starmerge.lib.tw_merge import merge, tailwind_merge
from starmerge.lib.validators import (
    is_any,
    is_any_non_arbitrary,
    is_arbitrary_image,
    is_arbitrary_length,
    is_arbitrary_number,
    is_arbitrary_position,
    is_arbitrary_shadow,
    is_arbitrary_size,
    is_arbitrary_value,
    is_arbitrary_variable,
    is_arbitrary_variable_family_name,
    is_arbitrary_variable_image,
    is_arbitrary_variable_length,
    is_arbitrary_variable_position,
    is_arbitrary_variable_shadow,
    is_arbitrary_variable_size,
    is_color,
    is_fraction,
    is_image,
    is_integer,
    is_length,
    is_length_only,
    is_never,
    is_number,
    is_percent,
    is_shadow,
    is_tshirt_size,
)

__version__ = version("starmerge")

__all__ = [
    "create_tailwind_merge",
    "tw_join",
    "ClassNameValue",
    "get_default_config",
    "tailwind_merge",
    "merge",
    "extend_tailwind_merge",
    "merge_configs",
    "from_theme",
    "validators",
    "is_arbitrary_value",
    "is_length",
    "is_tshirt_size",
    "is_any",
    "is_color",
    "is_number",
    "is_integer",
    "is_percent",
    "is_arbitrary_number",
    "is_arbitrary_length",
    "is_arbitrary_position",
    "is_arbitrary_size",
    "is_arbitrary_shadow",
    "is_arbitrary_image",
    "is_arbitrary_variable",
    "is_arbitrary_variable_family_name",
    "is_arbitrary_variable_image",
    "is_arbitrary_variable_length",
    "is_arbitrary_variable_position",
    "is_arbitrary_variable_shadow",
    "is_arbitrary_variable_size",
    "is_fraction",
    "is_image",
    "is_shadow",
    "is_never",
    "is_any_non_arbitrary",
    "is_length_only",
    "create_parse_class_name",
    "IMPORTANT_MODIFIER",
]
