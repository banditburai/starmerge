"""Extend Tailwind Merge with custom configurations."""

from typing import Any, Callable, List, Optional, Union

from starmerge.lib.create_tailwind_merge import create_tailwind_merge, CreateConfigSubsequent
from starmerge.lib.default_config import get_default_config
from starmerge.lib.merge_configs import merge_configs
from starmerge.lib.types import AnyConfig, ConfigExtension, TailwindMerge
from starmerge.lib.tw_merge import tailwind_merge as default_tailwind_merge


def extend_tailwind_merge(
    config_extension: Union[ConfigExtension, Callable[[AnyConfig], AnyConfig]],
    *create_config: CreateConfigSubsequent
) -> TailwindMerge:
    default_config = get_default_config()

    if callable(config_extension):
        def create_config_fn():
            return config_extension(default_config.copy())
        return create_tailwind_merge(create_config_fn, *create_config)
    else:
        def create_merged_config():
            config_copy = default_config.copy()
            return merge_configs(config_copy, config_extension)
        return create_tailwind_merge(create_merged_config, *create_config)
