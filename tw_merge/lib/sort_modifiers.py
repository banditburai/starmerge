"""
Sort modifiers utility for tailwind-merge.

This module provides functionality for sorting Tailwind CSS modifiers
according to the configured rules. Position-sensitive modifiers
(arbitrary variants and specified sensitive modifiers) are preserved
in their original position, while other modifiers are sorted alphabetically.
"""

from typing import List, Callable, Dict

from tw_merge.lib.types import AnyConfig


def create_sort_modifiers(config: AnyConfig) -> Callable[[List[str]], List[str]]:
    """
    Create a function for sorting modifiers according to configured rules.
    
    Sorts modifiers according to following schema:
    - Predefined modifiers are sorted alphabetically
    - When an arbitrary variant appears, it must be preserved which modifiers are before and after it
    - Position-sensitive modifiers (configured in orderSensitiveModifiers) must maintain their order
    
    Args:
        config: The tailwind-merge configuration
        
    Returns:
        A function that sorts modifiers
    """
    # Create a dictionary for fast lookup of order-sensitive modifiers
    order_sensitive_modifiers: Dict[str, bool] = {}
    
    # Handle both camelCase and snake_case keys for backward compatibility
    sensitive_modifiers = config.get('order_sensitive_modifiers', 
                                    config.get('orderSensitiveModifiers', []))
    
    for modifier in sensitive_modifiers:
        order_sensitive_modifiers[modifier] = True
    
    def sort_modifiers(modifiers: List[str]) -> List[str]:
        """
        Sort modifiers according to configured rules.
        
        Args:
            modifiers: List of modifiers to sort
            
        Returns:
            Sorted list of modifiers
        """
        if len(modifiers) <= 1:
            return modifiers
        
        sorted_modifiers: List[str] = []
        unsorted_modifiers: List[str] = []
        
        for modifier in modifiers:
            # Check if modifier is position-sensitive (arbitrary variant or configured as sensitive)
            is_position_sensitive = (
                modifier.startswith('[') or 
                modifier in order_sensitive_modifiers
            )
            
            if is_position_sensitive:
                # Sort accumulated non-sensitive modifiers and add them
                sorted_modifiers.extend(sorted(unsorted_modifiers))
                # Add the position-sensitive modifier
                sorted_modifiers.append(modifier)
                # Reset unsorted modifiers
                unsorted_modifiers = []
            else:
                # Accumulate non-sensitive modifiers for later sorting
                unsorted_modifiers.append(modifier)
        
        # Add any remaining unsorted modifiers
        sorted_modifiers.extend(sorted(unsorted_modifiers))
        
        return sorted_modifiers
    
    return sort_modifiers
