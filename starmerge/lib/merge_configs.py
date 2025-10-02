"""Merge configurations for tailwind-merge, extending and overriding defaults."""

from typing import Any, Dict, List, Optional, TypeVar, Union, cast

from starmerge.lib.types import AnyConfig, ConfigExtension

T = TypeVar('T')
K = TypeVar('K', bound=str)


def merge_configs(
    base_config: AnyConfig,
    config_extension: Union[ConfigExtension, callable]
) -> AnyConfig:
    if callable(config_extension):
        return config_extension(base_config)

    cache_size = config_extension.get('cache_size', config_extension.get('cacheSize'))
    prefix = config_extension.get('prefix')
    separator = config_extension.get('separator')
    experimental_parse_class_name = config_extension.get('experimental_parse_class_name', 
                                                        config_extension.get('experimentalParseClassName'))
    extend = config_extension.get('extend', {})
    override = config_extension.get('override', {})

    override_property(base_config, 'cache_size', cache_size)
    override_property(base_config, 'cacheSize', cache_size)
    override_property(base_config, 'prefix', prefix)
    override_property(base_config, 'separator', separator)
    override_property(base_config, 'experimental_parse_class_name', experimental_parse_class_name)
    override_property(base_config, 'experimentalParseClassName', experimental_parse_class_name)

    theme_key = 'theme'
    class_groups_key = 'classGroups' if 'classGroups' in base_config else 'class_groups'
    conflicting_class_groups_key = 'conflictingClassGroups' if 'conflictingClassGroups' in base_config else 'conflicting_class_groups'
    conflicting_class_group_modifiers_key = 'conflictingClassGroupModifiers' if 'conflictingClassGroupModifiers' in base_config else 'conflicting_class_group_modifiers'
    order_sensitive_modifiers_key = 'orderSensitiveModifiers' if 'orderSensitiveModifiers' in base_config else 'order_sensitive_modifiers'

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

    merge_config_properties(base_config.get(theme_key, {}), extend.get('theme', {}))
    merge_config_properties(base_config.get(class_groups_key, {}), 
                           extend.get('classGroups', extend.get('class_groups', {})))
    merge_config_properties(base_config.get(conflicting_class_groups_key, {}),
                           extend.get('conflictingClassGroups', extend.get('conflicting_class_groups', {})))

    extend_modifiers = extend.get('conflictingClassGroupModifiers', extend.get('conflicting_class_group_modifiers', {}))
    for key, value in extend_modifiers.items():
        if key not in base_config.get(conflicting_class_group_modifiers_key, {}):
            base_config[conflicting_class_group_modifiers_key][key] = value
        else:
            for v in value:
                if v not in base_config[conflicting_class_group_modifiers_key][key]:
                    base_config[conflicting_class_group_modifiers_key][key].append(v)

    extend_order_modifiers = extend.get('orderSensitiveModifiers', extend.get('order_sensitive_modifiers', []))
    if extend_order_modifiers:
        if order_sensitive_modifiers_key not in base_config:
            base_config[order_sensitive_modifiers_key] = []
        base_config[order_sensitive_modifiers_key].extend(extend_order_modifiers)

    return base_config


def override_property(base_object: Dict[str, Any], override_key: str, override_value: Any) -> None:
    if override_value is not None:
        base_object[override_key] = override_value


def override_config_properties(
    base_object: Dict[str, List[Any]],
    override_object: Optional[Dict[str, List[Any]]]
) -> None:
    if not override_object:
        return

    for key, value in override_object.items():
        if value is not None:
            base_object[key] = value


def merge_config_properties(
    base_object: Dict[str, List[Any]],
    merge_object: Optional[Dict[str, List[Any]]]
) -> None:
    if not merge_object:
        return

    for key, value in merge_object.items():
        if key not in base_object:
            base_object[key] = value
        elif isinstance(base_object[key], list) and isinstance(value, list):
            base_object[key] = base_object[key] + value
        elif isinstance(base_object[key], dict) and isinstance(value, dict):
            merge_config_properties(base_object[key], value)
        else:
            base_object[key] = value


def merge_array_properties(
    base_object: Dict[str, Any],
    merge_object: Dict[str, Any],
    key: str
) -> None:
    if key not in merge_object:
        return
    
    merge_value = merge_object[key]

    if key not in base_object:
        base_object[key] = merge_value
        return

    base_value = base_object[key]

    if isinstance(base_value, list) and isinstance(merge_value, list):
        base_object[key] = base_value + merge_value
    elif isinstance(base_value, dict) and isinstance(merge_value, dict):
        for merge_key, merge_value_inner in merge_value.items():
            if merge_key not in base_value:
                base_value[merge_key] = merge_value_inner
            elif isinstance(base_value[merge_key], list) and isinstance(merge_value_inner, list):
                base_value[merge_key] = base_value[merge_key] + merge_value_inner
            else:
                base_value[merge_key] = merge_value_inner
    else:
        base_object[key] = merge_value
