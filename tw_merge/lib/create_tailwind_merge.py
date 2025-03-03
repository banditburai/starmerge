"""
Create Tailwind Merge function generator.

This module provides a function to create a TailwindMerge function that
merges multiple tailwind class lists into a single class list, handling
conflicts according to the configured rules.
"""

from typing import Any, Callable, List, TypeVar, Dict, cast

from tw_merge.lib.config_utils import create_config_utils, ConfigUtils
from tw_merge.lib.merge_classlist import merge_class_list
from tw_merge.lib.tw_join import tw_join, ClassNameValue
from tw_merge.lib.types import AnyConfig


# Type definitions
CreateConfigFirst = Callable[[], AnyConfig]
CreateConfigSubsequent = Callable[[AnyConfig], AnyConfig]
TailwindMerge = Callable[..., str]


# Create a class wrapper for ConfigUtils dictionary to allow attribute access
class ConfigUtilsWrapper:
    """Wrapper class for ConfigUtils dictionary to allow attribute access."""
    
    def __init__(self, config_utils_dict: Dict[str, Any]):
        """
        Initialize ConfigUtilsWrapper with a ConfigUtils dictionary.
        
        Args:
            config_utils_dict: Dictionary containing configuration utilities
        """
        self.config_utils_dict = config_utils_dict
    
    def __getattr__(self, name: str) -> Any:
        """
        Get an attribute from the ConfigUtils dictionary.
        
        Args:
            name: Name of the attribute
            
        Returns:
            The attribute value
            
        Raises:
            AttributeError: If the attribute does not exist
        """
        if name in self.config_utils_dict:
            return self.config_utils_dict[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


def create_tailwind_merge(
    create_config_first: CreateConfigFirst,
    *create_config_rest: CreateConfigSubsequent
) -> TailwindMerge:
    """
    Create a tailwind merge function based on the provided configuration functions.
    
    Args:
        create_config_first: Function that creates the initial configuration
        *create_config_rest: Functions that modify the configuration
        
    Returns:
        A function that merges tailwind class lists
    """
    # Initialize variables in outer scope
    config_utils_wrapper = None
    cache_get = None
    cache_set = None
    
    def init_tailwind_merge(class_list: str) -> str:
        """
        Initialize the tailwind merge function with the provided configuration.
        
        Args:
            class_list: Space-separated string of class names
            
        Returns:
            A merged string with conflicts resolved
        """
        nonlocal config_utils_wrapper, cache_get, cache_set, function_to_call
        
        # Reduce the configuration functions to a single configuration
        # Apply each function in sequence to build the final config
        config = create_config_first()
        for create_config_current in create_config_rest:
            config = create_config_current(config)
        
        # Create configuration utilities
        config_utils_dict = create_config_utils(config)
        config_utils_wrapper = ConfigUtilsWrapper(config_utils_dict)
        cache_get = config_utils_dict['cache'].get
        cache_set = config_utils_dict['cache'].set
        function_to_call = tailwind_merge
        
        return tailwind_merge(class_list)
    
    def tailwind_merge(class_list: str) -> str:
        """
        Merge a class list using the configured rules and caching.
        
        Args:
            class_list: Space-separated string of class names
            
        Returns:
            A merged string with conflicts resolved
        """
        # Check cache first
        cached_result = cache_get(class_list)
        
        if cached_result:
            return cached_result
        
        # Merge class list and cache result
        result = merge_class_list(class_list, config_utils_wrapper)
        cache_set(class_list, result)
        
        return result
    
    def call_tailwind_merge(*args: ClassNameValue) -> str:
        """
        Call the appropriate function with joined arguments.
        
        Args:
            *args: Class name values to merge
            
        Returns:
            A merged string with conflicts resolved
        """
        return function_to_call(tw_join(*args))
    
    # Set the initial function to call
    function_to_call = init_tailwind_merge
    
    return call_tailwind_merge
