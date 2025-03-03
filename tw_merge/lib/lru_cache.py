"""
LRU cache implementation for tailwind-merge.

This module provides a Least Recently Used (LRU) cache implementation
inspired by hashlru (https://github.com/dominictarr/hashlru)
but using Python dictionaries for better performance.
"""

from typing import Dict, Generic, Optional, Protocol, TypeVar, Callable, Any

# Define generic type variables
K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type


class LruCache(Protocol, Generic[K, V]):
    """
    Protocol defining the interface for an LRU cache.
    """
    def get(self, key: K) -> Optional[V]:
        """
        Get a value from the cache by key.
        
        Args:
            key: The key to look up
            
        Returns:
            The cached value or None if not found
        """
        ...
    
    def set(self, key: K, value: V) -> None:
        """
        Set a value in the cache.
        
        Args:
            key: The key to store the value under
            value: The value to store
        """
        ...


class DefaultLruCache(Generic[K, V]):
    """
    Default implementation of an LRU cache.
    
    This implementation uses two dictionaries to efficiently manage cache entries.
    When the cache reaches its maximum size, the older dictionary is cleared
    and the dictionaries are swapped.
    """
    
    def __init__(self, max_cache_size: int):
        """
        Initialize a new LRU cache.
        
        Args:
            max_cache_size: Maximum number of items to store in the cache
        """
        self.max_cache_size = max_cache_size
        self.cache_size = 0
        self.cache: Dict[K, V] = {}
        self.previous_cache: Dict[K, V] = {}
    
    def _update(self, key: K, value: V) -> None:
        """
        Update the cache with a new key-value pair.
        
        If adding this item exceeds the max cache size, the older cache
        is discarded and a new empty cache is created.
        
        Args:
            key: The key to update
            value: The value to store
        """
        self.cache[key] = value
        self.cache_size += 1
        
        if self.cache_size > self.max_cache_size:
            self.cache_size = 0
            self.previous_cache = self.cache
            self.cache = {}
    
    def get(self, key: K) -> Optional[V]:
        """
        Get a value from the cache by key.
        
        If the key is in the previous cache but not the current one,
        it will be moved to the current cache.
        
        Args:
            key: The key to look up
            
        Returns:
            The cached value or None if not found
        """
        # Try to get the value from the current cache
        value = self.cache.get(key)
        
        if value is not None:
            return value
            
        # If not in current cache, try previous cache
        value = self.previous_cache.get(key)
        
        if value is not None:
            # Move from previous to current cache
            self._update(key, value)
            return value
            
        return None
    
    def set(self, key: K, value: V) -> None:
        """
        Set a value in the cache.
        
        Args:
            key: The key to store the value under
            value: The value to store
        """
        # If key is in current cache, just update it
        if key in self.cache:
            self.cache[key] = value
        else:
            # Otherwise add it as a new entry
            self._update(key, value)


class EmptyLruCache(Generic[K, V]):
    """
    Empty implementation of LRU cache that doesn't actually cache anything.
    Used when cache size is < 1.
    """
    
    def get(self, key: K) -> Optional[V]:
        """Always returns None."""
        return None
    
    def set(self, key: K, value: V) -> None:
        """Does nothing."""
        pass


def create_lru_cache(max_cache_size: int) -> LruCache:
    """
    Create a new LRU cache with the specified maximum size.
    
    Args:
        max_cache_size: Maximum number of items to store in the cache.
            If < 1, returns a no-op cache that doesn't store anything.
    
    Returns:
        An LRU cache implementation
    """
    if max_cache_size < 1:
        return EmptyLruCache()
    
    return DefaultLruCache(max_cache_size)
