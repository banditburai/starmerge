from typing import Callable, Any
from functools import reduce

from .config_utils import create_config_utils
from .merge_classlist import merge_class_list
from .tw_join import tw_join, ClassNameValue
from .types import Config

# Type definitions
ConfigUtils = Any  # Will be replaced with proper type once config_utils is implemented
CreateConfigFirst = Callable[[], Config]
CreateConfigSubsequent = Callable[[Config], Config]
TailwindMerge = Callable[..., str]

def create_tailwind_merge(
    create_config_first: CreateConfigFirst,
    *create_config_rest: CreateConfigSubsequent
) -> TailwindMerge:
    """Creates a function that merges Tailwind CSS classes without style conflicts."""
    
    config_utils = None
    cache_get = None
    cache_set = None
    function_to_call = None
    
    def init_tailwind_merge(class_list: str) -> str:
        nonlocal config_utils, cache_get, cache_set, function_to_call
        
        config = reduce(
            lambda prev_config, create_config_current: create_config_current(prev_config),
            create_config_rest,
            create_config_first()
        )
        
        config_utils = create_config_utils(config)
        cache_get = config_utils['cache']['get']  # Changed to dictionary access
        cache_set = config_utils['cache']['set']  # Changed to dictionary access
        function_to_call = tailwind_merge
        
        return tailwind_merge(class_list)
    
    def tailwind_merge(class_list: str) -> str:
        cached_result = cache_get(class_list)
        
        if cached_result:
            return cached_result
            
        result = merge_class_list(class_list, config_utils)
        cache_set(class_list, result)
        
        return result
    
    function_to_call = init_tailwind_merge
    
    def call_tailwind_merge(*args: ClassNameValue) -> str:
        return function_to_call(tw_join(*args))
    
    return call_tailwind_merge