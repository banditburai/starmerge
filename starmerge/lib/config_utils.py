from collections.abc import Callable
from typing import TypedDict

from starmerge.lib.class_group_utils import create_class_group_utils
from starmerge.lib.lru_cache import LruCache, create_lru_cache
from starmerge.lib.parse_class_name import create_parse_class_name
from starmerge.lib.sort_modifiers import create_sort_modifiers
from starmerge.lib.types import AnyClassGroupIds, AnyConfig, ParsedClassName


class ConfigUtils(TypedDict):
    cache: LruCache[str, str]
    parse_class_name: Callable[[str], ParsedClassName]
    sort_modifiers: Callable[[list[str]], list[str]]
    get_class_group_id: Callable[[str], AnyClassGroupIds | None]
    get_conflicting_class_group_ids: Callable[
        [AnyClassGroupIds, bool], list[AnyClassGroupIds]
    ]


def create_config_utils(config: AnyConfig) -> ConfigUtils:
    get_class_group_id, get_conflicting_class_group_ids = create_class_group_utils(
        config
    )

    return {
        "cache": create_lru_cache(config.get("cache_size", 500)),
        "parse_class_name": create_parse_class_name(config),
        "sort_modifiers": create_sort_modifiers(config),
        "get_class_group_id": get_class_group_id,
        "get_conflicting_class_group_ids": get_conflicting_class_group_ids,
    }
