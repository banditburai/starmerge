from dataclasses import dataclass
from typing import Dict, List, Optional, Callable, Any, TypeVar, Union, Tuple
from .types import (
    ClassValidator,
    ClassGroup,
    ThemeGetter,
    ThemeObject,
    Config,
    ClassValidatorObject,
    ClassPartObject
)


CLASS_PART_SEPARATOR = '-'

def create_class_group_utils(config: Dict[str, Any]) -> Dict[str, Any]:
    class_map = create_class_map(config)
    conflicting_class_groups = config.get('conflicting_class_groups', {})
    conflicting_class_group_modifiers = config.get('conflicting_class_group_modifiers', {})

    def get_class_group_id(class_name: str) -> Optional[str]:
        class_parts = class_name.split(CLASS_PART_SEPARATOR)
        
        # Handle negative values like `-inset-1`
        if class_parts[0] == '' and len(class_parts) > 1:
            class_parts.pop(0)
            
        return (get_group_recursive(class_parts, class_map) or 
                get_group_id_for_arbitrary_property(class_name))


    def get_conflicting_class_group_ids(
        class_group_id: str,  # Changed from GenericClassGroupIds
        has_postfix_modifier: bool,
    ) -> List[str]:
        conflicts = conflicting_class_groups.get(class_group_id, [])
        
        if has_postfix_modifier and class_group_id in conflicting_class_group_modifiers:
            return [*conflicts, *conflicting_class_group_modifiers[class_group_id]]
            
        return conflicts

    return {
        'get_class_group_id': get_class_group_id,
        'get_conflicting_class_group_ids': get_conflicting_class_group_ids,
    }

def get_group_recursive(
    class_parts: List[str],
    class_part_object: Dict[str, Any]
) -> Optional[str]:
    if not class_parts:
        return class_part_object.get('class_group_id')
    
    current_class_part = class_parts[0]
    next_class_part_object = class_part_object['next_part'].get(current_class_part)
    
    if next_class_part_object:
        class_group_from_next_part = get_group_recursive(class_parts[1:], next_class_part_object)
        if class_group_from_next_part:
            return class_group_from_next_part
    
    validators = class_part_object.get('validators', [])
    if not validators:
        return None
        
    class_rest = CLASS_PART_SEPARATOR.join(class_parts)
    
    for validator in validators:
        validator_func = validator['validator']
        # Check if it's a theme getter
        if hasattr(validator_func, 'is_theme_getter'):
            # Theme getters should receive a dict, not a string
            if isinstance(validator_func.theme, dict):
                if validator_func(validator_func.theme):
                    return validator['class_group_id']
        # Regular validator
        elif validator_func(class_rest):
            return validator['class_group_id']
    
    return None

import re
ARBITRARY_PROPERTY_REGEX = re.compile(r'^\[(.+)\]$')

def get_group_id_for_arbitrary_property(class_name: str) -> Optional[str]:
    """Get group ID for arbitrary property classes like [property:value]."""
    match = ARBITRARY_PROPERTY_REGEX.match(class_name)
    if match:
        arbitrary_property_class_name = match.group(1)
        if arbitrary_property_class_name:
            property_end = arbitrary_property_class_name.find(':')
            if property_end != -1:
                property_name = arbitrary_property_class_name[:property_end]
                # Two dots used as prefix for class groups in plugins
                return f'arbitrary..{property_name}'
    return None

def create_class_map(config: Dict[str, Any]) -> Dict[str, Any]:
    """Create a class map from config."""
    theme = config['theme']
    prefix = config.get('prefix')
    
    class_map = {
        'next_part': {},
        'validators': [],  # Initialize empty validators list
        'class_group_id': None
    }
    
    prefixed_class_group_entries = get_prefixed_class_group_entries(
        list(config['class_groups'].items()),
        prefix
    )
    
    for class_group_id, class_group in prefixed_class_group_entries:
        process_classes_recursively(class_group, class_map, class_group_id, theme)
    
    return class_map

def process_classes_recursively(
    class_group: List[Any],
    class_part_object: Dict[str, Any],
    class_group_id: str,
    theme: Dict[str, Any]
) -> None:
    for class_definition in class_group:
        if isinstance(class_definition, str):
            class_part_object_to_edit = (
                class_part_object if class_definition == '' 
                else get_part(class_part_object, class_definition)
            )
            class_part_object_to_edit['class_group_id'] = class_group_id
            continue

        if callable(class_definition):
            if hasattr(class_definition, 'is_theme_getter'):
                process_classes_recursively(
                    class_definition(theme),
                    class_part_object,
                    class_group_id,
                    theme
                )
                continue

            if 'validators' not in class_part_object:
                class_part_object['validators'] = []
                
            class_part_object['validators'].append({
                'validator': class_definition,
                'class_group_id': class_group_id
            })
            continue

        for key, value in class_definition.items():
            process_classes_recursively(
                value,
                get_part(class_part_object, key),
                class_group_id,
                theme
            )

def get_part(class_part_object: Dict[str, Any], path: str) -> Dict[str, Any]:
    current = class_part_object
    
    for path_part in path.split(CLASS_PART_SEPARATOR):
        if 'next_part' not in current:
            current['next_part'] = {}
        if path_part not in current['next_part']:
            current['next_part'][path_part] = {
                'next_part': {},
                'validators': [],
                'class_group_id': None
            }
        current = current['next_part'][path_part]
    
    return current

def is_theme_getter(func: Union[ClassValidator, ThemeGetter]) -> bool:
    """Check if a function is a theme getter."""
    return hasattr(func, 'is_theme_getter')

def get_prefixed_class_group_entries(
    class_group_entries: List[Tuple[str, ClassGroup]],
    prefix: Optional[str]
) -> List[Tuple[str, ClassGroup]]:  
    """Add prefix to class group entries if prefix is defined."""
    if not prefix:
        return class_group_entries

    def prefix_class_definition(class_definition: Any) -> Any:
        if isinstance(class_definition, str):
            return prefix + class_definition
        if isinstance(class_definition, dict):
            return {
                prefix + key: value 
                for key, value in class_definition.items()
            }
        return class_definition

    return [
        (
            class_group_id,
            [prefix_class_definition(cd) for cd in class_group]
        )
        for class_group_id, class_group in class_group_entries
    ]