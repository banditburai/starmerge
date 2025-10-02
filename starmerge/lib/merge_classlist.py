"""Merge class list utility for handling Tailwind CSS class conflicts."""

import re
from typing import List, Dict, Set, Optional, Protocol, Any

from starmerge.lib.parse_class_name import IMPORTANT_MODIFIER
from starmerge.lib.types import AnyClassGroupIds

SPLIT_CLASSES_REGEX = re.compile(r'\s+')


class ConfigUtils(Protocol):
    """Protocol defining the required functions from config utils."""
    def parse_class_name(self, class_name: str) -> Any: ...
    def get_class_group_id(self, class_name: str) -> Optional[AnyClassGroupIds]: ...
    def get_conflicting_class_group_ids(
        self, class_group_id: AnyClassGroupIds, has_postfix_modifier: bool
    ) -> List[AnyClassGroupIds]: ...
    def sort_modifiers(self, modifiers: List[str]) -> List[str]: ...


def merge_class_list(class_list: str, config_utils: ConfigUtils) -> str:
    parse_class_name = config_utils.parse_class_name
    get_class_group_id = config_utils.get_class_group_id
    get_conflicting_class_group_ids = config_utils.get_conflicting_class_group_ids
    sort_modifiers = config_utils.sort_modifiers

    class_groups_in_conflict: List[str] = []
    
    class_names = SPLIT_CLASSES_REGEX.split(class_list.strip())


    result = ""

    for index in range(len(class_names) - 1, -1, -1):
        original_class_name = class_names[index]
        if not original_class_name:
            continue
            
        parsed = parse_class_name(original_class_name)

        if parsed["is_external"]:
            result = original_class_name + (" " + result if result else result)
            continue
            
        has_postfix_modifier = bool(parsed["maybe_postfix_modifier_position"])
        base_class_name = parsed["base_class_name"]

        if has_postfix_modifier:
            postfix_position = parsed["maybe_postfix_modifier_position"]
            class_group_id = get_class_group_id(base_class_name[:postfix_position])
        else:
            class_group_id = get_class_group_id(base_class_name)

        if not class_group_id:
            if not has_postfix_modifier:
                result = original_class_name + (" " + result if result else result)
                continue

            class_group_id = get_class_group_id(base_class_name)

            if not class_group_id:
                result = original_class_name + (" " + result if result else result)
                continue

            has_postfix_modifier = False

        variant_modifier = ":".join(sort_modifiers(parsed["modifiers"]))
        modifier_id = variant_modifier + IMPORTANT_MODIFIER if parsed["has_important_modifier"] else variant_modifier
        class_id = modifier_id + class_group_id

        if class_id in class_groups_in_conflict:
            continue

        class_groups_in_conflict.append(class_id)

        conflict_groups = get_conflicting_class_group_ids(class_group_id, has_postfix_modifier)
        for conflict_group in conflict_groups:
            conflict_id = modifier_id + conflict_group
            class_groups_in_conflict.append(conflict_id)

        result = original_class_name + (" " + result if result else result)
    
    return result
