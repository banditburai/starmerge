from collections.abc import Callable
from typing import Any

from starmerge.lib.types import AnyConfig, ConfigExtension


def merge_configs(
    base_config: AnyConfig,
    config_extension: ConfigExtension | Callable[..., AnyConfig],
) -> AnyConfig:
    if callable(config_extension):
        return config_extension(base_config)

    if (cache_size := config_extension.get('cache_size')) is not None:
        base_config['cache_size'] = cache_size
    if (prefix := config_extension.get('prefix')) is not None:
        base_config['prefix'] = prefix
    if (separator := config_extension.get('separator')) is not None:
        base_config['separator'] = separator
    if (experimental := config_extension.get('experimental_parse_class_name')) is not None:
        base_config['experimental_parse_class_name'] = experimental

    override = config_extension.get('override', {})
    extend = config_extension.get('extend', {})

    _override_config_properties(base_config.get('theme', {}), override.get('theme', {}))
    _override_config_properties(base_config.get('class_groups', {}), override.get('class_groups', {}))
    _override_config_properties(
        base_config.get('conflicting_class_groups', {}),
        override.get('conflicting_class_groups', {}),
    )
    _override_config_properties(
        base_config.get('conflicting_class_group_modifiers', {}),
        override.get('conflicting_class_group_modifiers', {}),
    )
    if order_override := override.get('order_sensitive_modifiers'):
        base_config['order_sensitive_modifiers'] = order_override

    _merge_config_properties(base_config.get('theme', {}), extend.get('theme', {}))
    _merge_config_properties(base_config.get('class_groups', {}), extend.get('class_groups', {}))
    _merge_config_properties(
        base_config.get('conflicting_class_groups', {}),
        extend.get('conflicting_class_groups', {}),
    )

    extend_modifiers = extend.get('conflicting_class_group_modifiers', {})
    base_modifiers = base_config.get('conflicting_class_group_modifiers', {})
    for key, value in extend_modifiers.items():
        existing = base_modifiers.setdefault(key, [])
        existing.extend(v for v in value if v not in existing)

    if extend_order := extend.get('order_sensitive_modifiers', []):
        base_config.setdefault('order_sensitive_modifiers', []).extend(extend_order)

    return base_config


def _override_config_properties(
    base_object: dict[str, list[Any]],
    override_object: dict[str, list[Any]] | None,
) -> None:
    if not override_object:
        return
    for key, value in override_object.items():
        if value is not None:
            base_object[key] = value


def _merge_config_properties(
    base_object: dict[str, list[Any]],
    merge_object: dict[str, list[Any]] | None,
) -> None:
    if not merge_object:
        return
    for key, value in merge_object.items():
        if key not in base_object:
            base_object[key] = value
        elif isinstance(base_object[key], list) and isinstance(value, list):
            base_object[key].extend(value)
        elif isinstance(base_object[key], dict) and isinstance(value, dict):
            _merge_config_properties(base_object[key], value)
        else:
            base_object[key] = value
