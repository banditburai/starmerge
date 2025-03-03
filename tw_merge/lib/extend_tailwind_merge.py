"""
Extend Tailwind Merge functionality.

This module provides a function to extend the default Tailwind Merge function
with custom configurations, allowing for customization of the merging behavior.
"""

from typing import Any, Callable, List, Optional, Union

from tw_merge.lib.create_tailwind_merge import create_tailwind_merge, CreateConfigSubsequent
from tw_merge.lib.default_config import get_default_config
from tw_merge.lib.merge_configs import merge_configs
from tw_merge.lib.types import AnyConfig, ConfigExtension, TailwindMerge
from tw_merge.lib.tw_merge import tailwind_merge as default_tailwind_merge


def extend_tailwind_merge(
    config_extension: Union[ConfigExtension, Callable[[AnyConfig], AnyConfig]],
    *create_config: CreateConfigSubsequent
) -> TailwindMerge:
    """
    Extend the default Tailwind Merge function with custom configurations.

    Args:
        config_extension: A configuration object or function to extend the default configuration
        *create_config: Additional configuration functions to apply

    Returns:
        A tailwind merge function with the extended configuration
    """
    # Get the default config
    default_config = get_default_config()
    
    if callable(config_extension):
        # If config_extension is a function, create a function that applies it to the default config
        def create_config_fn():
            return config_extension(default_config.copy())
        
        # Create a new tailwind merge function with the modified config
        return create_tailwind_merge(create_config_fn, *create_config)
    else:
        # Otherwise, merge the config_extension with the default config
        def create_merged_config():
            # Create a deep copy of the default config to avoid modifying it
            config_copy = default_config.copy()
            # Merge the config_extension into the copy
            return merge_configs(config_copy, config_extension)
        
        # Create a new tailwind merge function with the merged config
        return create_tailwind_merge(create_merged_config, *create_config)
