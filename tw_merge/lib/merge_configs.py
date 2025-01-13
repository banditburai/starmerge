from typing import TypeVar, Dict, List, Any, Optional, Union, TypedDict
from .types import ConfigExtension, GenericConfig

T = TypeVar('T')
K = TypeVar('K', bound=str)

def merge_configs(
    base_config: GenericConfig,
    config_extension: ConfigExtension
) -> GenericConfig:
    """
    Merge config extension into base config.
    
    Args:
        base_config: Config where other config will be merged into. This object will be mutated.
        config_extension: Partial config to merge into the base_config.
    
    Returns:
        The modified base_config
    """
    # Extract values with proper defaults
    cache_size = config_extension.get('cache_size')
    prefix = config_extension.get('prefix')
    separator = config_extension.get('separator')
    experimental_parse_class_name = config_extension.get('experimental_parse_class_name')
    extend = config_extension.get('extend', {})
    override = config_extension.get('override', {})

    # Override static properties
    if cache_size is not None:
        base_config['cache_size'] = cache_size
    if prefix is not None:
        base_config['prefix'] = prefix
    if separator is not None:
        base_config['separator'] = separator
    if experimental_parse_class_name is not None:
        base_config['experimental_parse_class_name'] = experimental_parse_class_name

    # Handle override and extend
    for config_key, override_value in override.items():
        if config_key in base_config:
            override_config_properties(base_config[config_key], override_value)

    for key, extend_value in extend.items():
        if key in base_config:
            merge_config_properties(base_config[key], extend_value)

    return base_config

def override_config_properties(
    base_object: Dict[str, List[Any]],
    override_object: Optional[Dict[str, List[Any]]]
) -> None:
    """Override config properties in base object with those from override object."""
    if override_object:
        base_object.update(override_object)

def merge_config_properties(
    base_object: Dict[str, List[Any]],
    merge_object: Optional[Dict[str, List[Any]]]
) -> None:
    """Merge config properties from merge object into base object."""
    if merge_object:
        for key, value in merge_object.items():
            if value is not None:
                base_object[key] = base_object.get(key, []) + value