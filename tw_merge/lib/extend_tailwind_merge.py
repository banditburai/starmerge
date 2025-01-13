from typing import Union, Callable, Any

from .create_tailwind_merge import create_tailwind_merge
from .default_config import get_default_config
from .merge_configs import merge_configs
from .types import Config

# Type aliases
CreateConfigSubsequent = Callable[[Config], Config]
ConfigOrCallable = Union[Config, CreateConfigSubsequent]

def extend_tailwind_merge(
    config_extension: ConfigOrCallable,
    *create_config: CreateConfigSubsequent
) -> Callable[..., str]:
    """Extends the default tailwind-merge configuration.
    
    Args:
        config_extension: Either a config extension object or a function that modifies the config
        create_config: Additional config modifier functions
    
    Returns:
        A tailwind merge function with the extended configuration
    """
    if callable(config_extension):
        return create_tailwind_merge(get_default_config, config_extension, *create_config)
    else:
        return create_tailwind_merge(
            lambda: merge_configs(get_default_config(), config_extension),
            *create_config
        )