from typing import TypeVar, Callable, Any, Dict
from dataclasses import dataclass

from .class_group_utils import create_class_group_utils
from .lru_cache import create_lru_cache
from .parse_class_name import create_parse_class_name

T = TypeVar('T')
CacheGet = Callable[[str], str | None]
CacheSet = Callable[[str, str], None]

@dataclass
class Cache:
    get: CacheGet
    set: CacheSet

class ConfigUtils:
    cache: Cache
    parse_class_name: Any  # Will be properly typed once parse_class_name is implemented
    get_class_group_id: Callable[[str], str | None]
    get_conflicting_class_group_ids: Callable[[str, bool], list[str]]

def create_config_utils(config: Dict[str, Any]) -> Dict[str, Any]:
    """Create configuration utilities."""
    cache = create_lru_cache(config['cache_size'])
    class_group_utils = create_class_group_utils(config)
    
    return {
        'cache': {
            'get': cache.get,
            'set': cache.set
        },
        'parse_class_name': create_parse_class_name(config),
        'get_class_group_id': class_group_utils['get_class_group_id'],
        'get_conflicting_class_group_ids': class_group_utils['get_conflicting_class_group_ids']
    }