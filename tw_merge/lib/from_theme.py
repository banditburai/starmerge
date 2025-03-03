"""
Theme getter utility for tailwind-merge.

This module provides a utility for creating theme getter functions
that can be used to access theme values in the configuration.
"""

from typing import Any, Dict, List, Protocol, Union

from tw_merge.lib.types import AnyThemeGroupIds, ThemeObject


class ThemeGetter(Protocol):
    """Theme getter function type."""
    
    isThemeGetter: bool
    
    def __call__(self, theme: ThemeObject) -> List[Any]:
        """
        Get values from a theme for a specific key.
        
        Args:
            theme: The theme object to get values from
            
        Returns:
            A list of values from the theme
        """
        ...


def from_theme(key: AnyThemeGroupIds) -> ThemeGetter:
    """
    Create a theme getter function for a specific theme key.
    
    Args:
        key: The theme key to get values for
        
    Returns:
        A theme getter function
    """
    def theme_getter(theme: Union[ThemeObject, Any]) -> List[Any]:
        """
        Get values from a theme for a specific key.
        
        Args:
            theme: The theme object to get values from
            
        Returns:
            A list of values from the theme
        """
        # Handle case where theme might be a string or other non-dictionary value
        if not isinstance(theme, dict):
            return []
        
        return theme.get(key, [])
    
    # Add is_theme_getter property to identify this as a theme getter
    setattr(theme_getter, 'is_theme_getter', True)
    
    return theme_getter  # type: ignore
