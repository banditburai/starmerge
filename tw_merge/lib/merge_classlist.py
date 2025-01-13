import re
from typing import List, Dict, Any

from .config_utils import ConfigUtils
from .parse_class_name import IMPORTANT_MODIFIER, sort_modifiers

SPLIT_CLASSES_REGEX = re.compile(r'\s+')

def merge_class_list(class_list: str, config_utils: Dict[str, Any]) -> str:
    """
    Merge Tailwind CSS classes handling conflicts appropriately.
    
    Args:
        class_list: Space-separated string of Tailwind CSS classes
        config_utils: Configuration utilities for parsing and handling classes
        
    Returns:
        Merged class string with conflicts resolved
    """
    parse_class_name = config_utils['parse_class_name']
    get_class_group_id = config_utils['get_class_group_id']
    get_conflicting_class_group_ids = config_utils['get_conflicting_class_group_ids']

    # Set of classGroupIds in format: {importantModifier}{variantModifiers}{classGroupId}
    # Examples: 'float', 'hover:focus:bg-color', 'md:!pr'
    class_groups_in_conflict: List[str] = []
    class_names = SPLIT_CLASSES_REGEX.split(class_list.strip())

    result = ''

    # Process classes from right to left to match Tailwind's behavior
    for original_class_name in reversed(class_names):
        parsed = parse_class_name(original_class_name)
        modifiers = parsed.modifiers
        has_important_modifier = parsed.has_important_modifier
        base_class_name = parsed.base_class_name
        maybe_postfix_modifier_position = parsed.maybe_postfix_modifier_position

        has_postfix_modifier = bool(maybe_postfix_modifier_position)
        class_group_id = get_class_group_id(
            base_class_name[:maybe_postfix_modifier_position]
            if has_postfix_modifier
            else base_class_name
        )

        if not class_group_id:
            if not has_postfix_modifier:
                # Not a Tailwind class
                result = original_class_name + (' ' + result if result else '')
                continue

            class_group_id = get_class_group_id(base_class_name)

            if not class_group_id:
                # Not a Tailwind class
                result = original_class_name + (' ' + result if result else '')
                continue

            has_postfix_modifier = False

        variant_modifier = ':'.join(sort_modifiers(modifiers))
        modifier_id = variant_modifier + IMPORTANT_MODIFIER if has_important_modifier else variant_modifier
        class_id = modifier_id + class_group_id

        if class_id in class_groups_in_conflict:
            # Tailwind class omitted due to conflict
            continue

        class_groups_in_conflict.append(class_id)

        conflict_groups = get_conflicting_class_group_ids(class_group_id, has_postfix_modifier)
        for group in conflict_groups:
            class_groups_in_conflict.append(modifier_id + group)

        # Tailwind class not in conflict
        result = original_class_name + (' ' + result if result else '')

    return result 