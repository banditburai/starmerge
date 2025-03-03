"""
Merge configurations for tailwind-merge.

This module provides functions to merge configurations for tailwind-merge,
allowing for extending and overriding the default configuration.
"""

from typing import Any, Dict, List, Optional, TypeVar, Union, cast

from tw_merge.lib.types import AnyConfig, ConfigExtension

T = TypeVar('T')
K = TypeVar('K', bound=str)


def merge_configs(
    base_config: AnyConfig,
    config_extension: Union[ConfigExtension, callable]
) -> AnyConfig:
    """
    Merge a config extension into a base config.

    Args:
        base_config: Config where other config will be merged into. This object will be mutated.
        config_extension: Partial config to merge into the `base_config`.

    Returns:
        The merged configuration.
    """
    # Handle function config
    if callable(config_extension):
        return config_extension(base_config)

    # Extract values from config_extension
    cache_size = config_extension.get('cache_size', config_extension.get('cacheSize'))
    prefix = config_extension.get('prefix')
    separator = config_extension.get('separator')
    experimental_parse_class_name = config_extension.get('experimental_parse_class_name', 
                                                        config_extension.get('experimentalParseClassName'))
    extend = config_extension.get('extend', {})
    override = config_extension.get('override', {})

    # Override top-level properties
    override_property(base_config, 'cache_size', cache_size)
    override_property(base_config, 'cacheSize', cache_size)
    override_property(base_config, 'prefix', prefix)
    override_property(base_config, 'separator', separator)
    override_property(base_config, 'experimental_parse_class_name', experimental_parse_class_name)
    override_property(base_config, 'experimentalParseClassName', experimental_parse_class_name)

    # Determine which keys to use based on what's in the base_config
    theme_key = 'theme'
    class_groups_key = 'classGroups' if 'classGroups' in base_config else 'class_groups'
    conflicting_class_groups_key = 'conflictingClassGroups' if 'conflictingClassGroups' in base_config else 'conflicting_class_groups'
    conflicting_class_group_modifiers_key = 'conflictingClassGroupModifiers' if 'conflictingClassGroupModifiers' in base_config else 'conflicting_class_group_modifiers'
    order_sensitive_modifiers_key = 'orderSensitiveModifiers' if 'orderSensitiveModifiers' in base_config else 'order_sensitive_modifiers'

    # Override nested properties
    override_config_properties(base_config.get(theme_key, {}), override.get('theme', {}))
    override_config_properties(base_config.get(class_groups_key, {}), override.get('classGroups', override.get('class_groups', {})))
    override_config_properties(base_config.get(conflicting_class_groups_key, {}), 
                              override.get('conflictingClassGroups', override.get('conflicting_class_groups', {})))
    override_config_properties(
        base_config.get(conflicting_class_group_modifiers_key, {}),
        override.get('conflictingClassGroupModifiers', override.get('conflicting_class_group_modifiers', {}))
    )
    override_property(base_config, order_sensitive_modifiers_key, 
                     override.get('orderSensitiveModifiers', override.get('order_sensitive_modifiers')))

    # Extend nested properties
    merge_config_properties(base_config.get(theme_key, {}), extend.get('theme', {}))
    merge_config_properties(base_config.get(class_groups_key, {}), 
                           extend.get('classGroups', extend.get('class_groups', {})))
    merge_config_properties(base_config.get(conflicting_class_groups_key, {}), 
                           extend.get('conflictingClassGroups', extend.get('conflicting_class_groups', {})))
    
    # Special handling for conflicting_class_group_modifiers to match TypeScript behavior
    extend_modifiers = extend.get('conflictingClassGroupModifiers', extend.get('conflicting_class_group_modifiers', {}))
    for key, value in extend_modifiers.items():
        if key not in base_config.get(conflicting_class_group_modifiers_key, {}):
            base_config[conflicting_class_group_modifiers_key][key] = value
        else:
            # Append values if they don't already exist
            for v in value:
                if v not in base_config[conflicting_class_group_modifiers_key][key]:
                    base_config[conflicting_class_group_modifiers_key][key].append(v)
                    
    # Special handling for order_sensitive_modifiers to match TypeScript behavior
    extend_order_modifiers = extend.get('orderSensitiveModifiers', extend.get('order_sensitive_modifiers', []))
    if extend_order_modifiers:
        if order_sensitive_modifiers_key not in base_config:
            base_config[order_sensitive_modifiers_key] = []
        base_config[order_sensitive_modifiers_key].extend(extend_order_modifiers)

    return base_config


def override_property(base_object: Dict[str, Any], override_key: str, override_value: Any) -> None:
    """
    Override a property in a base object if the override value is not None.

    Args:
        base_object: The object to modify
        override_key: The key to override
        override_value: The value to set
    """
    # In TypeScript, undefined (None in Python) doesn't remove keys
    # Only set if override_value is not None
    if override_value is not None:
        base_object[override_key] = override_value


def override_config_properties(
    base_object: Dict[str, List[Any]],
    override_object: Optional[Dict[str, List[Any]]]
) -> None:
    """
    Override properties from an override object in a base object.

    Args:
        base_object: The object to modify
        override_object: The object containing values to override
    """
    if not override_object:
        return

    for key, value in override_object.items():
        # In TypeScript, undefined/null values don't remove keys
        if value is not None:
            base_object[key] = value


def merge_config_properties(
    base_object: Dict[str, List[Any]],
    merge_object: Optional[Dict[str, List[Any]]]
) -> None:
    """
    Merge properties from merge_object into base_object.

    Args:
        base_object: The object to merge into
        merge_object: The object to merge from
    """
    if not merge_object:
        return

    for key, value in merge_object.items():
        if key not in base_object:
            # If the key doesn't exist in the base object, just set it
            base_object[key] = value
        elif isinstance(base_object[key], list) and isinstance(value, list):
            # For arrays, concatenate them
            base_object[key] = base_object[key] + value
        elif isinstance(base_object[key], dict) and isinstance(value, dict):
            # For nested objects, recursively merge them
            merge_config_properties(base_object[key], value)
        else:
            # For other values, just set the merge value
            base_object[key] = value


def merge_array_properties(
    base_object: Dict[str, Any],
    merge_object: Dict[str, Any],
    key: str
) -> None:
    """
    Merge array properties from merge_object into base_object.

    Args:
        base_object: The object to merge into
        merge_object: The object to merge from
        key: The key of the property to merge
    """
    if key not in merge_object:
        return
    
    merge_value = merge_object[key]
    
    if key not in base_object:
        # If the key doesn't exist in the base object, just set it
        base_object[key] = merge_value
        return
    
    base_value = base_object[key]
    
    # If both values are arrays, concatenate them
    if isinstance(base_value, list) and isinstance(merge_value, list):
        base_object[key] = base_value + merge_value
    
    # If both values are dictionaries, merge them deeper
    elif isinstance(base_value, dict) and isinstance(merge_value, dict):
        for merge_key, merge_value_inner in merge_value.items():
            if merge_key not in base_value:
                # If the key doesn't exist in the base value, just set it
                base_value[merge_key] = merge_value_inner
            elif isinstance(base_value[merge_key], list) and isinstance(merge_value_inner, list):
                # If both values are arrays, concatenate them
                base_value[merge_key] = base_value[merge_key] + merge_value_inner
            else:
                # For other values, just set the merge value
                base_value[merge_key] = merge_value_inner
    
    # For other types, overwrite
    else:
        base_object[key] = merge_value
