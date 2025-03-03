"""
Utilities for working with class groups.

This module provides utilities for working with class groups, such as creating
the class map, getting class group IDs, and getting conflicting class group IDs.
"""

from dataclasses import dataclass, field
from enum import StrEnum
import re
from typing import Dict, List, Optional, Any, Set, Callable, Union, TypeAlias

from tw_merge.lib.types import (
    AnyClassGroupIds,
    ClassGroup,
    ClassGroupIds,
    ClassMap,
    ClassValidator,
    Config,
    ConflictingClassGroupIds,
    ThemeGetter,
    ThemeObject,
)

# Type aliases for complex types
ClassGroupGetter: TypeAlias = Callable[[str], Optional[AnyClassGroupIds]]
ConflictGetter: TypeAlias = Callable[[AnyClassGroupIds, bool], List[AnyClassGroupIds]]

class Separators(StrEnum):
    """Constants used for class name separation and property handling."""
    CLASS_PART = '-'
    EMPTY = ''
    ARBITRARY = '..'

# Regular expressions
ARBITRARY_PROPERTY_REGEX = re.compile(r'^\[(.+)\]$')

# At the top with other constants
MAX_RECURSION_DEPTH = 100

class TailwindMergeError(Exception):
    """Base exception for tw_merge errors."""

class MaxRecursionError(TailwindMergeError):
    """Raised when maximum recursion depth is exceeded."""

class CircularReferenceError(TailwindMergeError):
    """Raised when a circular reference is detected."""

@dataclass(frozen=True)
class ClassValidatorObject:
    """
    Object containing a class group ID and its validator function.
    
    Attributes:
        class_group_id: The ID of the class group this validator belongs to
        validator: Function that validates if a class belongs to this group
    """
    class_group_id: AnyClassGroupIds
    validator: ClassValidator

@dataclass
class ClassPartObject:
    """
    Object representing a part of a class name with its associated validators and next parts.
    
    This is used to recursively build the class map for resolving class group IDs.
    
    Attributes:
        next_part: Dictionary mapping to next parts in the class hierarchy
        validators: List of validators for this class part
        class_group_id: Optional ID of the class group this part belongs to
    """
    next_part: Dict[str, 'ClassPartObject'] = field(default_factory=dict)
    validators: List[ClassValidatorObject] = field(default_factory=list)
    class_group_id: Optional[AnyClassGroupIds] = None

def create_class_group_utils(config: Config) -> tuple[ClassGroupGetter, ConflictGetter]:
    """Create utilities for working with Tailwind CSS class groups.
    
    Args:
        config: Configuration dictionary containing class groups and conflict rules
        
    Returns:
        A tuple of (get_class_group_id, get_conflicting_class_group_ids) functions for
        resolving class groups and their conflicts
    """
    class_map = create_class_map(config)
    
    # Handle both camelCase and snake_case keys for backward compatibility
    conflicting_class_groups = config.get('conflicting_class_groups', 
                                         config.get('conflictingClassGroups', {}))
    conflicting_class_group_modifiers = config.get('conflicting_class_group_modifiers', 
                                                  config.get('conflictingClassGroupModifiers', {}))
    order_sensitive_modifiers = config.get('order_sensitive_modifiers', 
                                          config.get('orderSensitiveModifiers', []))

    def get_class_group_id(class_name: str) -> Optional[AnyClassGroupIds]:
        """Get the class group ID for a given class name."""

        class_parts = class_name.split(Separators.CLASS_PART)

        # Classes like `-inset-1` produce an empty string as first class_part.
        # We assume that classes for negative values are used correctly and remove it from class_parts.
        if class_parts[0] == '' and len(class_parts) != 1:
            class_parts.pop(0)

        return (get_group_recursive(class_parts, class_map) or 
                get_group_id_for_arbitrary_property(class_name))

    def get_conflicting_class_group_ids(
        class_group_id: AnyClassGroupIds,
        has_postfix_modifier: bool,
    ) -> List[AnyClassGroupIds]:
        """Get the conflicting class group IDs for a given class group ID."""
        conflicts = conflicting_class_groups.get(class_group_id, [])

        if has_postfix_modifier and class_group_id in conflicting_class_group_modifiers:
            return conflicts + conflicting_class_group_modifiers[class_group_id]

        return conflicts

    return get_class_group_id, get_conflicting_class_group_ids


def get_group_recursive(
    class_parts: List[str],
    class_part_object: ClassPartObject,
) -> Optional[AnyClassGroupIds]:
    """Recursively get the class group ID for a list of class parts."""
    if not class_parts: 
        return class_part_object.class_group_id

    current_class_part = class_parts[0]
    if next_class_part_object := class_part_object.next_part.get(current_class_part):  # Walrus operator
        if class_group_from_next := get_group_recursive(class_parts[1:], next_class_part_object):
            return class_group_from_next

    if not class_part_object.validators: 
        return None

    class_rest = Separators.CLASS_PART.join(class_parts)
    for validator_obj in class_part_object.validators:
        if validator_obj.validator(class_rest):
            return validator_obj.class_group_id
    
    return None


# Regular expression for arbitrary property classes like '[bg:red]'
arbitrary_property_regex = re.compile(r'^\[(.+)\]$')


def get_group_id_for_arbitrary_property(class_name: str) -> Optional[str]:
    """Get the class group ID for an arbitrary property class."""

    match = arbitrary_property_regex.match(class_name)
    if match:
        arbitrary_property_class_name = match.group(1)
        if arbitrary_property_class_name and ':' in arbitrary_property_class_name:
            property_name = arbitrary_property_class_name.split(':', 1)[0]
            # Using two dots here because one dot is used as prefix for class groups in plugins
            return f'arbitrary..{property_name}'
    
    return None


def create_class_map(config: Config) -> ClassPartObject:
    """
    Create a class map from the configuration.
    
    Args:
        config: The tailwind-merge configuration
        
    Returns:
        A ClassPartObject representing the root of the class map
    """
    theme = config.get('theme', {})
    
    # Handle both camelCase and snake_case keys for backward compatibility
    class_groups = config.get('class_groups', config.get('classGroups', {}))
    
    class_map = ClassPartObject()

    for class_group_id, class_group in class_groups.items():
        process_classes_recursively(class_group, class_map, class_group_id, theme)

    return class_map


def process_classes_recursively(
    class_definition: Union[Dict, List, ClassValidator, str],
    class_part_object: ClassPartObject,
    class_group_id: Optional[AnyClassGroupIds] = None,
    theme: Optional[Dict[str, Any]] = None,
    depth: int = 0,
    visited: Optional[Set[str]] = None
) -> None:
    """Process a class definition recursively."""
    if depth > MAX_RECURSION_DEPTH:
        return
    
    if visited is None:
        visited = set()
        
    if theme is None:
        theme = {}

    match class_definition:
        case str():
            class_part_object_to_edit = (
                class_part_object
                if class_definition == Separators.EMPTY
                else get_part(class_part_object, class_definition, depth + 1, visited)
            )
            class_part_object_to_edit.class_group_id = class_group_id
            
        case _ if callable(class_definition):
            if is_theme_getter(class_definition):
                process_classes_recursively(
                    class_definition(theme),
                    class_part_object,
                    class_group_id,
                    theme,
                    depth + 1,
                    visited
                )
            else:
                class_part_object.validators.append(
                    ClassValidatorObject(
                        class_group_id=class_group_id,
                        validator=class_definition,
                    )
                )
                
        case list():
            for sub_def in class_definition:
                process_classes_recursively(
                    sub_def,
                    class_part_object,
                    class_group_id,
                    theme,
                    depth + 1,
                    visited
                )
                
        case dict():
            for key, sub_group in class_definition.items():
                key_visited = visited.copy()
                process_classes_recursively(
                    sub_group,
                    get_part(class_part_object, key, depth + 1, key_visited),
                    class_group_id,
                    theme,
                    depth + 1,
                    key_visited
                )

def get_part(
    class_part_object: ClassPartObject,
    path: str,
    depth: int = 0,
    visited: Optional[Set[str]] = None
) -> ClassPartObject:
    """Get or create a part of the class map."""

    if depth > MAX_RECURSION_DEPTH:
        raise MaxRecursionError("Maximum recursion depth exceeded in get_part")
    
    visited = visited or set()
    
    if path in visited:
        return class_part_object
    
    visited.add(path)
    
    current_object = class_part_object
    for path_part in path.split(Separators.CLASS_PART):
        current_object = current_object.next_part.setdefault(
            path_part,
            ClassPartObject()
        )

    return current_object

def is_theme_getter(func: Union[ClassValidator, ThemeGetter]) -> bool:
    """Check if a function is a theme getter."""
    return hasattr(func, 'is_theme_getter') and bool(getattr(func, 'is_theme_getter'))
