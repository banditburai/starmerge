from typing import Protocol


class LruCache[K, V](Protocol):
    def get(self, key: K) -> V | None: ...
    def set(self, key: K, value: V) -> None: ...


class DefaultLruCache[K, V]:
    """Two-dict LRU: when max size is reached, the older dict is swapped out."""

    def __init__(self, max_cache_size: int):
        self.max_cache_size = max_cache_size
        self.cache_size = 0
        self.cache: dict[K, V] = {}
        self.previous_cache: dict[K, V] = {}

    def _update(self, key: K, value: V) -> None:
        self.cache[key] = value
        self.cache_size += 1

        if self.cache_size > self.max_cache_size:
            self.cache_size = 0
            self.previous_cache = self.cache
            self.cache = {}

    def get(self, key: K) -> V | None:
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


class EmptyLruCache[K, V]:
    def get(self, key: K) -> V | None:
        return None

    def set(self, key: K, value: V) -> None:
        pass


def create_lru_cache(max_cache_size: int) -> LruCache:
    if max_cache_size < 1:
        return EmptyLruCache()
    return DefaultLruCache(max_cache_size)
