"""Python port of the tailwind-merge library for efficiently merging Tailwind CSS classes."""
from . import validators
from .validators import *
from .parse_class_name import create_parse_class_name, IMPORTANT_MODIFIER
from .lru_cache import create_lru_cache
from .tw_join import tw_join
from .class_group_utils import create_class_group_utils
from .merge_classlist import merge_class_list
from .config_utils import create_config_utils
from .sort_modifiers import create_sort_modifiers
from .default_config import get_default_config
from .tw_merge import tailwind_merge, merge
from .extend_tailwind_merge import extend_tailwind_merge
from .merge_configs import merge_configs

__all__ = [
    'validators',
    'create_parse_class_name',
    'create_lru_cache',
    'tw_join',
    'create_class_group_utils',
    'merge_class_list',
    'create_config_utils',
    'create_sort_modifiers',
    'IMPORTANT_MODIFIER',
    'get_default_config',
    'tailwind_merge',
    'merge',
    'extend_tailwind_merge',
    'merge_configs',
]
