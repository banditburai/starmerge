"""
Main exports for tailwind-merge.
"""

from .lib.create_tailwind_merge import create_tailwind_merge
from .lib.default_config import get_default_config
from .lib.extend_tailwind_merge import extend_tailwind_merge
from .lib.from_theme import from_theme
from .lib.merge_configs import merge_configs
from .lib.tw_join import tw_join, ClassNameValue
from .lib.tw_merge import tw_merge
from .lib.types import (
    ClassValidator,
    Config,
    ConfigStatic,
    ConfigGroups,
    DefaultClassGroupIds,
    DefaultThemeGroupIds,
    ThemeGetter,
    ClassGroup,
    ThemeObject,
    GenericConfig,
)
from .lib import validators

__all__ = [
    'create_tailwind_merge',
    'get_default_config',
    'extend_tailwind_merge',
    'from_theme',
    'merge_configs',
    'tw_join',
    'tw_merge',
    'ClassNameValue',
    'ClassValidator',
    'Config',
    'ConfigStatic',
    'ConfigGroups',
    'DefaultClassGroupIds',
    'DefaultThemeGroupIds',
    'ThemeGetter',
    'ClassGroup',
    'ThemeObject',
    'GenericConfig',
    'validators',
]