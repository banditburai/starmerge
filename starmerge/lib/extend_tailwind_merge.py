from starmerge.lib.create_tailwind_merge import (
    CreateConfigSubsequent,
    create_tailwind_merge,
)
from starmerge.lib.default_config import get_default_config
from starmerge.lib.merge_configs import merge_configs
from starmerge.lib.types import ConfigExtension, TailwindMerge


def extend_tailwind_merge(
    config_extension: ConfigExtension | CreateConfigSubsequent,
    *create_config: CreateConfigSubsequent,
) -> TailwindMerge:
    default_config = get_default_config()

    if callable(config_extension):
        return create_tailwind_merge(
            lambda: config_extension(default_config.copy()), *create_config
        )

    return create_tailwind_merge(
        lambda: merge_configs(default_config.copy(), config_extension),
        *create_config,
    )
