"""
LRU cache implementation inspired by hashlru but using Python dictionaries.
https://github.com/dominictarr/hashlru
"""

from typing import Dict, Generic, Optional, Protocol, TypeVar, Callable, Any

K = TypeVar('K')
V = TypeVar('V')


class LruCache(Protocol, Generic[K, V]):
    """Protocol defining the interface for an LRU cache."""
    def get(self, key: K) -> Optional[V]: ...
    def set(self, key: K, value: V) -> None: ...


class DefaultLruCache(Generic[K, V]):
    """
    LRU cache using two dictionaries for efficiency.
    When max size is reached, the older dictionary is cleared and swapped.
    """

    def __init__(self, max_cache_size: int):
        self.max_cache_size = max_cache_size
        self.cache_size = 0
        self.cache: Dict[K, V] = {}
        self.previous_cache: Dict[K, V] = {}

    def _update(self, key: K, value: V) -> None:
        self.cache[key] = value
        self.cache_size += 1
        
        if self.cache_size > self.max_cache_size:
            self.cache_size = 0
            self.previous_cache = self.cache
            self.cache = {}

    def get(self, key: K) -> Optional[V]:
        value = self.cache.get(key)
        if value is not None:
            return value

        value = self.previous_cache.get(key)
        if value is not None:
            self._update(key, value)
            return value

        return None

    def set(self, key: K, value: V) -> None:
        if key in self.cache:
            self.cache[key] = value
        else:
            self._update(key, value)


class EmptyLruCache(Generic[K, V]):
    """No-op cache used when cache size is < 1."""
    def get(self, key: K) -> Optional[V]:
        return None
    def set(self, key: K, value: V) -> None:
        pass


def create_lru_cache(max_cache_size: int) -> LruCache:
    if max_cache_size < 1:
        return EmptyLruCache()
    
    return DefaultLruCache(max_cache_size)
