from typing import TypeVar, Optional, Dict, Protocol

K = TypeVar('K')
V = TypeVar('V')

class LruCache(Protocol[K, V]):
    """Protocol defining the interface for the LRU cache."""
    def get(self, key: K) -> Optional[V]: ...
    def set(self, key: K, value: V) -> None: ...

def create_lru_cache(max_cache_size: int) -> LruCache[K, V]:
    """
    Create an LRU cache with a maximum size.
    
    Inspired by hashlru (https://github.com/dominictarr/hashlru)
    but using Dict instead of Map for Python implementation.
    """
    if max_cache_size < 1:
        return type('EmptyCache', (), {
            'get': lambda self, key: None,
            'set': lambda self, key, value: None,
        })()

    class LruCacheImpl(LruCache[K, V]):
        def __init__(self):
            self.cache_size = 0
            self.cache: Dict[K, V] = {}
            self.previous_cache: Dict[K, V] = {}

        def update(self, key: K, value: V) -> None:
            self.cache[key] = value
            self.cache_size += 1

            if self.cache_size > max_cache_size:
                self.cache_size = 0
                self.previous_cache = self.cache
                self.cache = {}

        def get(self, key: K) -> Optional[V]:
            value = self.cache.get(key)
            if value is not None:
                return value
                
            value = self.previous_cache.get(key)
            if value is not None:
                self.update(key, value)
                return value
            return None

        def set(self, key: K, value: V) -> None:
            if key in self.cache:
                self.cache[key] = value
            else:
                self.update(key, value)

    return LruCacheImpl()