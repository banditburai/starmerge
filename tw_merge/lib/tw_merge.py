"""
Main API for tailwind-merge.

This module exposes the primary tailwind-merge function and related utilities.
"""

from typing import Optional, overload, List, Union, Any

from tw_merge.lib.create_tailwind_merge import create_tailwind_merge
from tw_merge.lib.default_config import get_default_config
from tw_merge.lib.types import TailwindMerge
from tw_merge.lib.tw_join import tw_join


def _create_tailwind_merge() -> TailwindMerge:
    """
    Create the default tailwind-merge function.
    
    Returns:
        The default tailwind-merge function.
    """
    tailwind_merge_fn = create_tailwind_merge(get_default_config)
    
    # Attach the config for potential extensions
    tailwind_merge_fn.config = get_default_config()  # type: ignore
    
    return tailwind_merge_fn


# Create default tailwind-merge function
tailwind_merge = _create_tailwind_merge()


@overload
def tw_merge(*args: str) -> str:
    ...


@overload
def tw_merge(class_list: List[Any]) -> str:
    ...


def tw_merge(*args: Any) -> str:
    """
    Merge Tailwind CSS classes without style conflicts.
    
    This function can be called with multiple string arguments or a single list of class names.
    It also supports nested arrays similar to the JavaScript implementation.
    
    Args:
        *args: Either multiple string arguments, a single list of class names,
               or any combination of strings, lists, and nested lists.
        
    Returns:
        A string of merged class names.
        
    Examples:
        >>> tw_merge("bg-red-500", "bg-blue-500")
        'bg-blue-500'
        
        >>> tw_merge(["text-sm", "text-lg"])
        'text-lg'
        
        >>> tw_merge("grow", [None, False, [["grow-[2]"]]])
        'grow-[2]'
    """
    # If there are no arguments, return an empty string
    if not args:
        return ""
        
    # If the first argument is a list and it's the only argument, process it as a list
    if len(args) == 1 and isinstance(args[0], list):
        classes = tw_join(args[0])
        return tailwind_merge(classes)
    
    # Process all arguments (strings, lists, etc.) with tw_join
    classes = tw_join(*args)
    return tailwind_merge(classes)


# Export the default instance and related utilities
__all__ = ["tailwind_merge", "tw_merge"]
