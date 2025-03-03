"""
Merge class list utility for tailwind-merge.

This module provides the functionality to merge multiple Tailwind CSS class names,
handling conflicts according to the configured rules. It processes a space-separated
list of class names and returns a merged string with conflicts resolved.
"""

import re
from typing import List, Dict, Set, Optional, Protocol, Any

from tw_merge.lib.parse_class_name import IMPORTANT_MODIFIER
from tw_merge.lib.types import AnyClassGroupIds


# Regular expression for splitting class names by whitespace
SPLIT_CLASSES_REGEX = re.compile(r'\s+')


class ConfigUtils(Protocol):
    """Protocol defining the required functions from config utils."""
    
    def parse_class_name(self, class_name: str) -> Any: 
        """Parse a class name into its components."""
        ...
    
    def get_class_group_id(self, class_name: str) -> Optional[AnyClassGroupIds]: 
        """Get the class group ID for a class name."""
        ...
    
    def get_conflicting_class_group_ids(
        self, class_group_id: AnyClassGroupIds, has_postfix_modifier: bool
    ) -> List[AnyClassGroupIds]: 
        """Get conflicting class group IDs for a class group ID."""
        ...
    
    def sort_modifiers(self, modifiers: List[str]) -> List[str]: 
        """Sort modifiers according to configured rules."""
        ...


def merge_class_list(class_list: str, config_utils: ConfigUtils) -> str:
    """
    Merge a space-separated list of class names, handling conflicts.
    
    Args:
        class_list: Space-separated string of class names
        config_utils: Utilities for working with class groups
        
    Returns:
        A merged string with conflicts resolved
    """
    parse_class_name = config_utils.parse_class_name
    get_class_group_id = config_utils.get_class_group_id
    get_conflicting_class_group_ids = config_utils.get_conflicting_class_group_ids
    sort_modifiers = config_utils.sort_modifiers
    
    # Set of class group IDs in following format:
    # `{importantModifier}{variantModifiers}{classGroupId}`
    # Example: 'float'
    # Example: 'hover:focus:bg-color'
    # Example: 'md:!pr'
    class_groups_in_conflict: List[str] = []
    
    class_names = SPLIT_CLASSES_REGEX.split(class_list.strip())
    
    result = ""
    
    # Process classes in reverse order (last one has highest precedence)
    for index in range(len(class_names) - 1, -1, -1):
        original_class_name = class_names[index]
        if not original_class_name:
            continue
            
        parsed = parse_class_name(original_class_name)
        
        if parsed["is_external"]:
            # External classes aren't processed for conflicts
            result = original_class_name + (" " + result if result else result)
            continue
            
        has_postfix_modifier = bool(parsed["maybe_postfix_modifier_position"])
        base_class_name = parsed["base_class_name"]
        
        # Get the class group ID
        if has_postfix_modifier:
            postfix_position = parsed["maybe_postfix_modifier_position"]
            class_group_id = get_class_group_id(base_class_name[:postfix_position])
        else:
            class_group_id = get_class_group_id(base_class_name)
            
        # Handle non-Tailwind classes
        if not class_group_id:
            if not has_postfix_modifier:
                # Not a Tailwind class
                result = original_class_name + (" " + result if result else result)
                continue
                
            # Try without assuming postfix modifier
            class_group_id = get_class_group_id(base_class_name)
            
            if not class_group_id:
                # Not a Tailwind class
                result = original_class_name + (" " + result if result else result)
                continue
                
            has_postfix_modifier = False
            
        # Get the variant modifier
        variant_modifier = ":".join(sort_modifiers(parsed["modifiers"]))
        
        # Add important modifier if present
        modifier_id = variant_modifier + IMPORTANT_MODIFIER if parsed["has_important_modifier"] else variant_modifier
        
        # Create the class ID
        class_id = modifier_id + class_group_id
        
        # Check if this class conflicts with any previously seen class
        if class_id in class_groups_in_conflict:
            # Tailwind class omitted due to conflict
            continue
            
        # Add this class to the conflicts list to mark it as seen
        class_groups_in_conflict.append(class_id)
        
        # Add conflicting class groups to the conflict list
        conflict_groups = get_conflicting_class_group_ids(class_group_id, has_postfix_modifier)
        for conflict_group in conflict_groups:
            conflict_id = modifier_id + conflict_group
            class_groups_in_conflict.append(conflict_id)
            
        # The class doesn't conflict with previously seen classes, include it
        result = original_class_name + (" " + result if result else result)
    
    return result
